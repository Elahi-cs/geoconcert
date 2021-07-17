from os import environ
from flask import url_for

class Config(object):
    
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "./.flask_session/"
    SECRET_KEY = environ['SECRET_KEY']

    # SPOTIFY CONFIG
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("CLIENT_SECRET")
    SCOPE = 'user-top-read'

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