#!/usr/bin/env bash

set -e

ssh cv \
  cd /srv/http/clients; \
  git pull; \
  poetry shell; \
  poetry update; \
  ./manage.py migrate; \
  ./manage.py compilemessages -l es &> /dev/null; \
  ./manage.py collectstatic --noinput; \
   supervisorctl restart clients:
