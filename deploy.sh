#!/usr/bin/env bash

set -e

f=0 b=0 s= h=

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -f|--frontend) f=1 ;;
        -b|--backend) b=1 ;;
        -s) s="$2"; shift ;;
        -h) h="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$s" ]
then
echo 'server name not provided'
exit 1
fi

if [ -z "$h" ]
then
echo 'host not provided'
exit 1
fi

echo start deploy to server $s with host $h

if [ $f == 1 ]
then
echo deploying frontend
cd frontend
BACKEND_HOST=$h NODE_ENV=production yarn run generate
cd ..
rsync -rvzz --delete -e ssh frontend/dist/ --exclude 'media' "$s":/var/django/clients/static
fi

if [ $b == 1 ]
then
echo deploying backend

ssh "$s" "\
  source .zprofile; \
  cd /srv/http/clients; \
  git pull; \
  source .venv/bin/activate; \
  poetry install --no-dev --no-root; \
  ./manage.py migrate; \
  ./manage.py compilemessages -l es &> /dev/null; \
  ./manage.py collectstatic --noinput; \
   supervisorctl restart clients:"
fi