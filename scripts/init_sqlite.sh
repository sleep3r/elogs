#!/usr/bin/env bash
cd ../mysite
python manage.py migrate
mv db.sqlite3 ../elog/db.sqlite3
cd ../elog
