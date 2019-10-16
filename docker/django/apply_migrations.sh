#!/usr/bin/env bash

echo "Executing migrations..."
python3 manage.py flush --noinput
python3 manage.py makemigrations --merge
python3 manage.py migrate
python3 manage.py demo_db --recreate
python3 manage.py shell < scripts/import_cells.py
