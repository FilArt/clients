#!/usr/bin/env bash

set -e

cd frontend

echo Input backend host
read -r BACKEND_HOST
echo Input server alias
read -r SERVER

BACKEND_HOST=$BACKEND_HOST NODE_ENV=production yarn run generate

cd ..

rsync -rvzz --delete -e ssh frontend/dist/ "$SERVER":/var/django/clients/static

ssh "$SERVER" "\
  cd /srv/http/clients; \
  git pull; \
  source .venv/bin/activate; \
  poetry install --no-dev --no-root; \
  ./manage.py migrate; \
  ./manage.py compilemessages -l es &> /dev/null; \
  ./manage.py collectstatic --noinput; \
   supervisorctl restart clients:"
