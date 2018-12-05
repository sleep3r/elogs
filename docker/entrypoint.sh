#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

#export CELERY_BROKER_URL="${REDIS_URL}"
#export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

cd /srv
python3.6 manage.py collectstatic --noinput
mkdir /srv/frontend/dist/static
cp -r /srv/staticfiles/* /srv/frontend/dist/static/

python3.6 manage.py makemigrations --merge
python3.6 manage.py migrate        # Apply database migrations
python3.6 manage.py demo_db --recreate

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

echo Starting Daphne...

exec daphne config.asgi:application \
    --bind 0.0.0.0 \
    --port 8001 \
    --verbosity 1 &

echo Starting Gunicorn...

exec gunicorn config.wsgi:application \
    --name e-logs \
    --bind "127.0.0.1:8002" \
    --workers 5 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log &

# exec celery -A e_logs.common.all_journals_app.tasks worker --loglevel=info &
# exec celery -A e_logs.common.all_journals_app.tasks beat --loglevel=info &

# lsof -i :8000

echo Starting node...
exec npm start --prefix /srv/e-logs-constructor/backend &

echo Starting caddy...
cd /srv
mv /srv/caddy /root/.caddy
exec caddy -quic -agree
# -log -quic stderr
# lsof -i :8000

