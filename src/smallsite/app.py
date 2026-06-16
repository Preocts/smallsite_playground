from __future__ import annotations

from wsgiref.simple_server import make_server
from pyramid.router import Router
from pyramid.config import Configurator

from .routes import ROUTES


def create_app() -> Router:
    """Create the WSGI app, load routes."""
    with Configurator() as config:

        for name, route, func in ROUTES:
            config.add_route(name, route)
            config.add_view(func, route_name=name)

        return config.make_wsgi_app()


def serve_forever() -> None:
    """Do just that."""
    app = create_app()

    server = make_server("127.0.0.1", 8000, app)

    try:
        print("small site runing. CTRL + C to exit")
        server.serve_forever()

    except KeyboardInterrupt:
        print()
