from __future__ import annotations

import sys

import waitress

from .app import create_app

# CLI options. If not provided, first in dict will be used.
_OPTIONS_MAP = {
    "local": {
        "listen": "127.0.0.1:8000",
    },
    "docker": {
        "listen": "0.0.0.0:8000",
    },
}


def serve() -> int:
    """Start serving with the correct options."""
    valid_flags = list(_OPTIONS_MAP)

    flag = sys.argv[1].lower() if len(sys.argv) > 1 else list(valid_flags)[0]

    if flag not in valid_flags:
        print(f"Unknown flag. Expected one of: {valid_flags}")
        return 1

    try:
        options = _OPTIONS_MAP[flag]
        print(f"smallsite running on {options['listen']}. CTRL + C to stop")
        waitress.serve(create_app(), **options)

    except KeyboardInterrupt:
        print("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(serve())
