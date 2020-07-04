#!/usr/bin/env bash

sleep 10    # wait until PostgreSQL will be ready to accept connections
python manage.py migrate
python manage.py collectstatic --no-input

set -euo pipefail
exec gunicorn --bind 0.0.0.0:8000 --worker-tmp-dir /dev/shm --workers=2 \
    --threads=4 --worker-class gthread \
    --log-file=- money_assistant.wsgi:application