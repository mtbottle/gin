#!/bin/sh
# script to (re)start the gin database with given data
python manage.py sqlclear gin_backend | python manage.py dbshell
python manage.py syncdb
python manage.py loaddata gin_backend/fixtures/seed.json
