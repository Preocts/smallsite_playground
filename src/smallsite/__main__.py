from __future__ import annotations

import sys

from wsgiref.simple_server import make_server
from gunicorn.app.base import BaseApplication
from pyramid.router import Router

from .app import create_app

_PROD_OPTIONS = {
    "bind": "0.0.0.0:8000",
}


# Source (ish) https://gunicorn.org/custom/
class StandaloneApplication(BaseApplication):

    def __init__(self, app: Router, options: None | dict[str, str] = None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def fast_serve() -> None:
    """Do just that."""
    server = make_server("127.0.0.1", 8000, create_app())

    try:
        print("small site runing. CTRL + C to exit")
        server.serve_forever()

    except KeyboardInterrupt:
        print()


def prod_serve() -> None:
    """Do just that."""
    StandaloneApplication(create_app(), _PROD_OPTIONS).run()


def dispatch() -> None:
    """Start the correct server."""
    flag = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    if flag != "prod":
        fast_serve()

    else:
        prod_serve()


if __name__ == "__main__":
    dispatch()
