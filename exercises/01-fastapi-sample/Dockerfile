ARG PYTHON_VERSION="3.8"

FROM python:${PYTHON_VERSION}-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install --no-install-recommends -y make curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY Makefile pyproject.toml uv.lock .integration ./

RUN uv sync --locked

CMD ["make", "test"]
