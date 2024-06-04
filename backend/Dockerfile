FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libreoffice \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app/

RUN pip install poetry watchdog \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

EXPOSE 2020