from __future__ import annotations

from pyramid.config import Configurator
from pyramid.router import Router

from .routes import ROUTES


def create_app() -> Router:
    """Create the WSGI app, load routes."""
    with Configurator() as config:

        for name, route, func in ROUTES:
            config.add_route(name, route)
            config.add_view(func, route_name=name)

        return config.make_wsgi_app()
