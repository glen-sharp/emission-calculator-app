#!/usr/bin/env bash

echo Delete SQLite DB file if present
rm db.sqlite3
echo

set -e

python manage.py test emission_calculator_backend/tests
echo -----------------
echo Unit tests passed
echo -----------------

python manage.py makemigrations
python manage.py migrate

python manage.py runscript import_data
echo
echo Data refresh complete