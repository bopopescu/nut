#!/usr/bin/env bash

python manage.py run_gunicorn --settings=settings.production --bind 0.0.0.0:8000