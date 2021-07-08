import os
import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    current_app,
)

import spotipy

bp = Blueprint('auth', __name__, url_prefix='/auth')

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def get_user_cache():
    return caches_folder + session.get('uuid')

@bp.route('/login')
def login():
    """
    Log user into Spotify, create session token
    
    https://github.com/plamere/spotipy/blob/master/examples/app.py
    """
    error = None
    if not session.get("uuid"):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=get_user_cache()
        )

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id=current_app.config["CLIENT_ID"],
        client_secret=current_app.config["CLIENT_SECRET"],
        redirect_uri=current_app.config["REDIRECT_URI"],
        scope=current_app.config["SCOPE"],
        cache_handler=cache_handler,
        show_dialog=True
    )

    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))


