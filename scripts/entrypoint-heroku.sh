#!/usr/bin/env bash

sleep 10    # wait until PostgreSQL will be ready to accept connections
python manage.py migrate
python manage.py collectstatic --no-input

exec gunicorn money_assistant.wsgi:application
