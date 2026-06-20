ARG DOCKER_IMAGE=python:3.14-alpine3.24
ARG UV_VERSION=0.11.8

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_image

FROM ${DOCKER_IMAGE} AS builder

COPY --from=uv_image /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

RUN touch README.md
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

COPY src src/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

FROM ${DOCKER_IMAGE} AS runner

RUN addgroup --gid 2000 app
RUN adduser --ingroup app --disabled-password --no-create-home --system --uid 2000 app

USER 2000:2000

WORKDIR /app

COPY --from=builder --chown=2000:2000 /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "smallsite", "docker"]
