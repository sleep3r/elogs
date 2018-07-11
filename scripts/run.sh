#! /bin/bash
webpack
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py my_command
python3 manage.py runserver
