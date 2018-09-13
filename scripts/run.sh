#! /bin/bash
webpack
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py demo_db --recreate -frac 1
python3 manage.py import_users
python3 manage.py runserver
