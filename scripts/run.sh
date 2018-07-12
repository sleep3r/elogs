#! /bin/bash
webpack
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py demo_db --recreate
python3 manage.py runserver
