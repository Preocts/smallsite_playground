from __future__ import annotations

from flask import Flask

from .routes import create_blueprint


def create_app() -> Flask:
    """Create the WSGI app, load routes."""
    app = Flask(__name__)

    app.register_blueprint(create_blueprint())

    return app
