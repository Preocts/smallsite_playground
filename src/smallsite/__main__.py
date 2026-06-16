from __future__ import annotations

from wsgiref.simple_server import make_server

from .app import site_app


def serve_forever() -> None:
    """Do just that."""
    server = make_server("127.0.0.1", 8000, site_app)

    try:
        print("small site runing. CTRL + C to exit")
        server.serve_forever()

    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    serve_forever()
