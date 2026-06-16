from __future__ import annotations

from wsgiref.simple_server import make_server

from .app import create_app


def serve_forever() -> None:
    """Do just that."""
    server = make_server("127.0.0.1", 8000, create_app())

    try:
        print("small site runing. CTRL + C to exit")
        server.serve_forever()

    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    serve_forever()
