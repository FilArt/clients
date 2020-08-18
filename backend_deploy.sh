#!/usr/bin/env bash

set -e

ssh cv "\
  cd /srv/http/clients; \
  git pull; \
  poetry install --no-dev --no-root; \
  ./manage.py migrate; \
  ./manage.py compilemessages -l es &> /dev/null; \
  ./manage.py collectstatic --noinput; \
   supervisorctl restart clients:"