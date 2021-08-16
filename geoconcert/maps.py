from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for,
    current_app, session
)
from werkzeug.exceptions import abort

import requests
import spotipy

from geoconcert.auth import login_required, get_user_cache, get_auth_manager

bp = Blueprint('maps', __name__)

@bp.route("/maps/preferences", methods=('GET', 'POST'))
@login_required
def preferences():
    # Avoid making an API call if the user returns to the preferences page
    if session.get("top_artists") is None:
        top_artists = get_top_artists()
        session["top_artists"] = top_artists
    else:
        top_artists = session["top_artists"]

    if request.method == 'POST':
        selected_artists = request.form.getlist('artists')
        session["artists"] = selected_artists
        return redirect(url_for('maps.geoconcert'))

    return render_template("maps/preferences.html", top_artists=top_artists)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():
    tm_root_url = current_app.config["TICKETMASTER_ROOT_URL"]
    tm_api_key = current_app.config["TICKETMASTER_KEY"]
    gmaps_key = current_app.config["GMAPS_KEY"]
    
    top_artists = session["artists"]
    concerts_info = {}
    found_event = False

    print(top_artists)
    #TODO: Handle the case where the user doesn't select an artist (better client-side)
    #TODO: Handle case where no events are found for selected artists
    for selected_artist in top_artists:
        payload = {'keyword': selected_artist}

        response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
                                params=payload)

        response_content = response.json()

        if response_content['page']['totalElements'] == 0:
            print(f"No events found for {selected_artist}!")
        else:
            found_event = True
            events = response_content["_embedded"]["events"]
            concerts_info[selected_artist] = {
                            "locations": [],
                            "concerts": [],
                            }
            for event in events: 
                location = get_location_from_event(event)
                concert = get_concert_info(event, location)

                # Append the information to a dict containing each concert and
                # location. They will be passed separately to different parts
                # of the GMaps JavaScript program.
                concerts_info[selected_artist]["locations"].append(location)
                concerts_info[selected_artist]["concerts"].append(concert)

    print(concerts_info)

    if not found_event:
        return render_template("maps/no_events.html", top_artists=top_artists)
    
    return render_template("maps/geoconcert.html", 
                concerts_info=concerts_info,
                gmaps_key=gmaps_key)

def get_location_from_event(event):
    """
    Append the coordinates of the event in a list of locations for the GMaps
    marker locations
    """
    location = {}
    coordinates = event["_embedded"]["venues"][0]["location"]
    location["lng"] = float(coordinates["longitude"])
    location["lat"] = float(coordinates["latitude"])
    return location

def get_concert_info(event, location):
    """Get additional information for each event for the markers' info window"""
    concert = {}
    concert["venue"] = event['_embedded']['venues'][0]['name']
    concert["location"] = location
    concert["city"] = event['_embedded']['venues'][0]['city']['name']
    concert["date"] = event['dates']['start']['localDate']
    concert["link"] = event["url"]
    return concert

def get_top_artists(all=False):
    """
    Make a call to the Spotify API to get the current user's top artists.
    
    Returns a dict with the user's top artists.

    Default is returning the user's medium term top artists unless ``all´´ is 
    True.
    """
    spotify = get_authenticated_client()

    if all:
        user_top_artists = {
            "short_term": [artist["name"] for artist in 
                    spotify.current_user_top_artists(time_range="short_term")["items"]],
            "medium_term": [artist["name"] for artist in
                    spotify.current_user_top_artists()["items"]],
            "long_term": [artist["name"] for artist in
                    spotify.current_user_top_artists(time_range="long_term")["items"]],
        }
        return user_top_artists

    return [artist["name"] for artist in spotify.current_user_top_artists()["items"]]

def get_authenticated_client():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
                    cache_path=get_user_cache())
    auth_manager = get_auth_manager(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    return spotipy.Spotify(auth_manager=auth_manager)
