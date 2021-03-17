#!/usr/bin/env bash

set -e

ssh $SERVER "\
  cd /srv/http/clients; \
  git pull; \
  source .venv/bin/activate; \
  poetry install --no-dev --no-root; \
  ./manage.py migrate; \
  ./manage.py compilemessages -l es &> /dev/null; \
  ./manage.py collectstatic --noinput; \
   supervisorctl restart clients:"
