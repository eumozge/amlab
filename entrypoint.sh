#!/bin/bash
export DJANGO_SETTINGS_MODULE=amlab.config.production

exec gunicorn amlab.wsgi:application \
    --name amlab \
    --bind 0.0.0.0:8000 \
    --preload \
    --chdir="./" \
    --workers 9
