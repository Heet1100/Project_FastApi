#!/usr/bin/env bash
: "${SERVICE:="benadmin-api"}"

if [ "$SERVICE" == "benadmin-api" ]; then
    # command bash -c "alembic upgrade head && gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9001"
    command bash -c "gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker -b $APP_HOST:$APP_PORT"

