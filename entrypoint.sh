#!/bin/bash
set -e

if [ "$1" = 'http' ]; then
  set -- python server.py
fi

if [ "$1" = 'bot' ]; then
  set -- python task_bot.py "$@"
fi

exec "$@"
