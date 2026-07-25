#!/bin/sh
set -e

poetry run alembic -c src/alembic.ini upgrade head

poetry run uvicorn main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload