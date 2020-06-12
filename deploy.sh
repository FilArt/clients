#!/usr/bin/env bash

set -e

cd frontend

NODE_ENV=production yarn run generate

cd ..

python manage.py collectstatic

rsync -rvzz --delete -e ssh frontend/dist/ cv:/var/django/clients

ssh cv "cd /srv/http/clients; git pull; venv/bin/python -m pip install -r requirements.txt; ./manage.py migrate; touch touch"

