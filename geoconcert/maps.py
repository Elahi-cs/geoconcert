from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for,
    current_app
)
from werkzeug.exceptions import abort

import requests

from geoconcert.auth import login_required

bp = Blueprint('maps', __name__)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():
    
    spotify_client = current_app.spotify_client

    spotify_call = spotify_client.current_user_top_artists()
    top_artists = []
    for artist in spotify_call["items"]:
        top_artists.append(artist["name"])
    print(top_artists)

    tm_root_url = current_app.config["TICKETMASTER_ROOT_URL"]
    tm_api_key = current_app.config["TICKETMASTER_KEY"]

    payload = {'keyword': top_artists[1]}

    response = requests.get(f"{tm_root_url}.json?apikey={tm_api_key}",
                            params=payload)

    print(response.json())

    return render_template("maps/geoconcert.html", top_artists=top_artists)