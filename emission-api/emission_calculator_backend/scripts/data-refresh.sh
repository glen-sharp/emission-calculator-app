#!/usr/bin/env bash

echo Delete SQLite DB file if present
rm db.sqlite3
echo

set -e

python manage.py makemigrations
python manage.py migrate

python manage.py runscript import_data
echo
echo Data refresh complete