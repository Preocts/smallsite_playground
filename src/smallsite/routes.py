from __future__ import annotations

import json

from flask import Response
from flask import Blueprint

OKAY_STATUS = {"status": "ok"}


def create_blueprint() -> Blueprint:
    """Creates Blueprint for defined routes."""

    bp = Blueprint("root", __name__, url_prefix="/")

    @bp.route("/", methods=["GET"])
    def default_route() -> Response:
        """Base route /"""
        body = "<html><body><h1>"
        body += "egg"
        body += "</h1></body></html>"
        return Response(body)

    @bp.route("/health", methods=["GET"])
    def health_check() -> Response:
        """Healthcheck route."""
        return Response(json.dumps(OKAY_STATUS), content_type="application/JSON")

    return bp
