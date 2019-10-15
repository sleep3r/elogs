#!/bin/bash
#sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -i './scripts/drop_db.sql'
psql -U elogs postgres -c 'DROP DATABASE elogs'
psql -U elogs postgres -c 'CREATE DATABASE elogs'
#python manage.py sqlflush | python manage.py dbshell
python manage.py flush --noinput
python manage.py migrate
python manage.py demo_db --recreate  --dashboard --formula
