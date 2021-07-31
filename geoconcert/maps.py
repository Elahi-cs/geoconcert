from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for,
    current_app
)
from werkzeug.exceptions import abort

import requests
import spotipy

from geoconcert.auth import login_required, get_user_cache, get_auth_manager

bp = Blueprint('maps', __name__)

@bp.route("/maps/preferences", methods=('GET', 'POST'))
@login_required
def preferences():
    top_artists = get_top_artists()
    if request.method == 'POST':
        return redirect(url_for('geoconcert'))

    return render_template("maps/preferences.html", top_artists=top_artists)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():

    tm_root_url = current_app.config["TICKETMASTER_ROOT_URL"]
    tm_api_key = current_app.config["TICKETMASTER_KEY"]
    gmaps_key = current_app.config["GMAPS_KEY"]
    
    top_artists = get_top_artists()

    print(top_artists)

    payload = {'keyword': top_artists[0]}

    response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
                            params=payload)

    response_content = response.json()

    locations = []

    if response_content['page']['totalElements'] == 0:
        print(f"No events found!")
    else:
        events = response_content["_embedded"]["events"]
        for event in events:
            locations.append(event["_embedded"]["venues"][0]["location"])        

    print(locations)

    return render_template("maps/geoconcert.html", top_artists=top_artists,
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
