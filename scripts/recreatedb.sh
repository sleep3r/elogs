#!/bin/bash
#sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -i './scripts/drop_db.sql'
#sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -Q 'DROP DATABASE elogs'
#sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -Q 'CREATE DATABASE elogs'
#python manage.py sqlflush | python manage.py dbshell
python manage.py flush --noinput
#python manage.py migrate
python manage.py demo_db --recreate
