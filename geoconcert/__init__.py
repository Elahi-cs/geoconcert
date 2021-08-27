import os

from flask import Flask, redirect, request

import config

def create_app(test_config=None):
    """
    This is an application factory. Any configuration, registration, and other
    setup the app needs will happen inside this function, then the application
    will be returned.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_object(config.ProdConfig)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def before_request():
        """Force HTTPS on Heroku."""
        # https://stackoverflow.com/questions/8436666/ ...
        # ... how-to-make-python-on-heroku-https-only
        # TODO: Check for a more permanent solution that works for all providers

        if 'DYNO' in os.environ:
            if request.url.startswith('http://'):
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)

    # a simple page that says hello, used to test app factory
    @app.route('/hello')
    def hello():
        return 'Hello, Flask.'

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule("/", endpoint='auth.index')

    from . import maps
    # maps references the main application behavior
    # (couldn't be called app for obvious reasons)
    app.register_blueprint(maps.bp)

    return app