#!/usr/bin/env bash
mv venv ../temp7453455
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
mv ../temp7453455 venv
