from __future__ import annotations

import json

from pyramid.response import Response
from pyramid.request import Request

_OKAY_STATUS = {"status": "ok"}


def _default_route(request: Request) -> Response:
    """Base route /"""
    body = "<html><body><h1>"
    body += "egg"
    body += "</h1></body></html>"
    return Response(body)


def _health_check(request: Request) -> Response:
    """Healthcheck route."""
    return Response(
        json.dumps(_OKAY_STATUS),
        content_type="application/JSON",
        charset="utf-8",
    )


ROUTES = [
    ("root", "/", _default_route),
    ("health", "/health", _health_check),
]
