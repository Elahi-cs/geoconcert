from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for,
    current_app
)
from werkzeug.exceptions import abort

from geoconcert.auth import login_required

bp = Blueprint('maps', __name__)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():
    
    spotify_client = current_app.spotify_client

    top_artists = spotify_client.current_user_top_artists()
    print(top_artists)

    return render_template("maps/geoconcert.html", top_artists=top_artists)