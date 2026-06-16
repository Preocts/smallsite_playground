from __future__ import annotations

import json

from pyramid.request import Request
from pyramid.response import Response

OKAY_STATUS = {"status": "ok"}


def health_check(request: Request) -> Response:
    """Healthcheck route."""
    return Response(json.dumps(OKAY_STATUS))


def default_route(request: Request) -> Response:
    """Base route /"""
    body = "<html><body><h1>"
    body += "egg"
    body += "</h1></body></html>"
    return Response(body)


ROUTES = [
    ("default", "/", default_route),
    ("health", "/health", health_check),
]
