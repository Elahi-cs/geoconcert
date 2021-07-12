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

@bp.route('/login')
def login():
    """
    Log user into Spotify, create session token
    
    https://github.com/plamere/spotipy/blob/master/examples/app.py
    """
    error = None
    if not session.get("uuid"):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = get_cache_file_handler(get_user_cache())

    auth_manager = get_auth_manager(cache_handler)

    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for("index"))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template("auth/login.html", auth_url=auth_url)

    spotify_client = spotipy.Spotify(auth_manager=auth_manager)

    try:
        user = spotify_client.me()
    except spotipy.exceptions.SpotifyException:
        error = "Login failed."
        return redirect(url_for("auth.logout"))

    username = user["display_name"]
    session["logged_in"] = True

    if error:
        flash(error)
    else:
        flash(f"Welcome, {username}.")

    return redirect(url_for("index"))

@bp.route('/logout')
def logout():
    """
    Delete cache, clean session.
    """
    try:
        os.remove(get_user_cache())
        session.clear()
    except OSError as error:
        print("Error: %s - %s." % (error.filename, error.strerror))
        flash("Error signing out, please try again.")

    return redirect(url_for("index"))

def get_user_cache():
    return caches_folder + session.get('uuid')

def get_cache_file_handler(cache_path):
    return spotipy.cache_handler.CacheFileHandler(
        cache_path=cache_path
        )

def get_auth_manager(cache_handler):
    """
    Returns a SpotifyOAuth object that implements Authorization Code Flow for 
    Spotify's OAuth implementation.

    This function exists because SpotifyOAuth objects store token info and so
    reusing a token could risk a leak of user info, so a new object needs to be
    created each time.
    """
    return spotipy.oauth2.SpotifyOAuth(
        client_id=current_app.config["CLIENT_ID"],
        client_secret=current_app.config["CLIENT_SECRET"],
        redirect_uri=current_app.config["REDIRECT_URI"],
        scope=current_app.config["SCOPE"],
        cache_handler=cache_handler,
        show_dialog=True
    )

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view