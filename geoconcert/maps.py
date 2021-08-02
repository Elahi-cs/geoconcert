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
    concert_locations = {}
    selected_artist = top_artists[0]

    print(top_artists)

    payload = {'keyword': selected_artist}

    response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
                            params=payload)

    response_content = response.json()

    if response_content['page']['totalElements'] == 0:
        print(f"No events found")
    else:
        events = response_content["_embedded"]["events"]
        for event in events:
            concert_locations[selected_artist] = {}
            coordinates = event["_embedded"]["venues"][0]["location"]
            concert_locations[selected_artist]["lng"] = \
                float(coordinates["longitude"])
            concert_locations[selected_artist]["lat"] = \
                float(coordinates["latitude"])

    print(concert_locations)

    """
    This is the code for the actual behavior. Since it makes an API call
    for each artist, I will be continuing development with a single call instead, 
    and then replace current code with this one when testing and in production.
    """
    # for artist in top_artists:
    #     payload = {'keyword': artist}
    #     response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
    #                             params=payload)
    #     response_content = response.json()
    #     if response_content['page']['totalElements'] == 0:
    #         print(f"No events found")
    #     else:
    #         events = response_content["_embedded"]["events"]
    #         for event in events:
    #             concert_locations[artist] = (event["_embedded"]["venues"][0]["location"]) 

    return render_template("maps/geoconcert.html", concert_locations=concert_locations,
                            gmaps_key=gmaps_key)


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
