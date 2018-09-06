#!/bin/bash
sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -Q 'DROP DATABASE elogs'
sqlcmd -S 127.0.0.1 -P 'Singapore2017' -U sa -Q 'CREATE DATABASE elogs'
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py demo_db --recreate -frac 10
