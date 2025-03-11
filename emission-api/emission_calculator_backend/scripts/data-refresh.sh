#!/usr/bin/env bash

# Enable exit on error
set -e

python manage.py test emission_calculator_backend/tests
echo -----------------
echo Unit tests passed
echo -----------------

# Disable exit on error for if SQLite file is not present
set +e

echo Delete SQLite DB file if present
rm db.sqlite3
echo

# Enable exit on error
set -e

python manage.py makemigrations
python manage.py migrate

python manage.py runscript import_data
echo
echo Data refresh complete