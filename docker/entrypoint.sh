#!/bin/bash

python3.6 manage.py makemigrations --merge
python3.6 manage.py migrate        # Apply database migrations
python3.6 manage.py demo_db --recreate

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

cp /srv/docker/django_nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
echo "daemon off;" >> /etc/nginx/nginx.conf
# Fix nginx errors (delete one bad line)
sed -i '/listen \[\:\:\]\:80 default_server;/d' /etc/nginx/sites-available/default

echo Starting Daphne...

exec daphne config.asgi:application \
    --bind 0.0.0.0 \
    --port 8001 \
    --verbosity 1 &

echo Starting Gunicorn...

exec gunicorn config.wsgi:application \
    --name e-logs \
    --bind unix:/srv/DigitalLogs.sock \
    --workers 5 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log &

# exec celery -A e_logs.common.all_journals_app.tasks worker --loglevel=info &
# exec celery -A e_logs.common.all_journals_app.tasks beat --loglevel=info &

echo Starting nginx...
exec service nginx start
