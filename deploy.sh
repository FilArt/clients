#!/usr/bin/env bash

set -e

cd frontend

NODE_ENV=production yarn run generate

cd ..

./manage.py collectstatic --noinput

rsync -rvzz --delete -e ssh frontend/dist/ cv:/var/django/clients/static

exec ./backend_deploy.sh
