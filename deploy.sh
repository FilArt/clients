#!/usr/bin/env bash

set -e

cd frontend

echo Input backend host
read BACKEND_HOST

BACKEND_HOST=$BACKEND_HOST NODE_ENV=production yarn run generate

cd ..

rsync -rvzz --delete -e ssh frontend/dist/ cv:/var/django/clients/static

exec ./backend_deploy.sh
