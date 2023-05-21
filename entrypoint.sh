#!/bin/bash
set -e

if [ "$1" = 'http' ]; then
  set -- uvicorn server:api_app --host 0.0.0.0 --port 8062
fi

if [ "$1" = 'bot' ]; then
  set -- python task_bot.py "$@"
fi

exec "$@"
