ARG DOCKER_IMAGE=python:3.13-alpine3.24
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
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev --group docker

COPY src src/
COPY smallsite_app.py ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable --group docker

# Download and build patchelf since selected version of alpine only ships iwth 0.18 and nuitka took that version personally.
ENV PATCHELF_VERSION=0.17.2 \
    PATCHELF_URL=https://github.com/NixOS/patchelf/archive/
RUN apk add --no-cache curl autoconf automake build-base
RUN curl -L ${PATCHELF_URL}${PATCHELF_VERSION}.tar.gz -o ${PATCHELF_VERSION}.tar.gz && \
    tar -xzf ${PATCHELF_VERSION}.tar.gz && \
    cd patchelf-${PATCHELF_VERSION} && \
    ./bootstrap.sh && \
    ./configure && \
    make && \
    make install && \
    cd ..

RUN uv run nuitka --mode=onefile --onefile-tempdir-spec=/tmp smallsite_app.py

RUN mkdir tmp

FROM scratch AS runner

COPY --from=builder /app/tmp /tmp/
COPY --from=builder /app/smallsite_app.bin /

# Fails here. I suspect this is due to the /tmp/jaraco/text/Lorem ipsum.txt having a space in it.
CMD ["/smallsite_app.bin", "docker"]
