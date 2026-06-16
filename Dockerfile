FROM python:3.14-alpine3.24 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev


COPY README.md ./
COPY src src/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

FROM python:3.14-alpine3.24 AS runner

ENV PATH="/app/.venv/bin:$PATH" \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

RUN addgroup --gid 2000 app
RUN adduser --no-create-home --system --uid 2000 app app

USER 2000:2000

WORKDIR /app

COPY --from=builder --chown=2000:2000 /app/.venv /app/.venv

EXPOSE 8000

CMD ["python", "-m", "smallsite", "prod"]
