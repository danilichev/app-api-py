FROM python:3.12.2-slim-bookworm AS base
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base AS install
WORKDIR /home/code

ARG INSTALL_ARGS="--no-root"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS

RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install as app-image

ENV PYTHONPATH=/home/code/ PYTHONHASHSEED=0

COPY alembic/ alembic/
COPY src/ src/
COPY tests/ tests/
COPY .env alembic.ini ./

RUN addgroup --system --gid 1001 "appuser"
RUN adduser --system --uid 1001 "appuser"
USER "appuser"
