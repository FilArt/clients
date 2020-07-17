#!/usr/bin/env bash

set -e

ssh cv "cd /srv/http/clients; git pull; venv/bin/python -m pip install -r requirements.txt; ./manage.py migrate; ./manage.py compilemessages -l ru -l es &> /dev/null; ./manage.py collectstatic --noinput; supervisorctl restart clients:"
