#!/usr/bin/env bash

set -e

cd frontend

NODE_ENV=production yarn run generate

cd ..

python manage.py collectstatic

rsync -rvzz --delete -e ssh frontend/dist/ cv:/var/django/clients

ssh cv "cd /srv/http/crm; git pull; ./manage.py migrate"