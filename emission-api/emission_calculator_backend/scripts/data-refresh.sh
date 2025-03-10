#!/usr/bin/env bash

set -e

rm db.sqlite3
echo SQLite DB deleted
echo

python manage.py makemigrations
python manage.py migrate

python manage.py runscript import_data
echo
echo Data refresh complete