from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for,
    current_app
)
from werkzeug.exceptions import abort

import requests
import spotipy

from geoconcert.auth import login_required, get_user_cache, get_auth_manager

bp = Blueprint('maps', __name__)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():
    
    spotify_call = get_top_artists()
    top_artists = []
    for artist in spotify_call["items"]:
        top_artists.append(artist["name"])

    tm_root_url = current_app.config["TICKETMASTER_ROOT_URL"]
    tm_api_key = current_app.config["TICKETMASTER_KEY"]

    payload = {'keyword': top_artists[1]}

    response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
                            params=payload)

    # if response.json()['page']['TotalElements'] == 0:
        

    print(response.json())

    return render_template("maps/geoconcert.html", top_artists=top_artists)

def get_top_artists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
                    cache_path=get_user_cache())
    auth_manager = get_auth_manager(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_top_artists()