ARG PYTHON_VERSION="3.8"

FROM python:${PYTHON_VERSION}-slim

ARG POETRY_HOME="/opt/poetry"
ARG POETRY_VERSION="1.5.1"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install --no-install-recommends -y make curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org/ | python3 - --version ${POETRY_VERSION} && \
    ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY Makefile pyproject.toml poetry.lock ./

RUN poetry install --no-root

CMD ["make", "test"]
