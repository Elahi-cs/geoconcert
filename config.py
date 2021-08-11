from os import environ
from flask import url_for

from dotenv import load_dotenv

load_dotenv("vars.env")

class Config(object):
    
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "./.flask_session/"
    SECRET_KEY = environ['SECRET_KEY']

    # SPOTIFY CONFIG
    SPOTIFY_CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    SCOPE = 'user-top-read'

    # TICKETMASTER CONFIG
    TICKETMASTER_KEY = environ.get("TICKETMASTER_KEY")
    TICKETMASTER_SECRET = environ.get("TICKETMASTER_SECRET")
    TICKETMASTER_ROOT_URL = "https://app.ticketmaster.com/discovery/v2/events"

    # GOOGLE MAPS CONFIG
    GMAPS_KEY = environ.get("GMAPS_KEY")

class ProdConfig(Config):
    """Deployment configuration."""

    TESTING = False
    DEBUG = False
    SHOW_DIALOG = False
    FLASK_ENV = "production"

class DevConfig(Config):
    """Development configuration."""

    TESTING = True
    DEBUG = True
    SHOW_DIALOG = True
    FLASK_ENV = "development"
    REDIRECT_URI = "http://127.0.0.1:5000/auth/login"