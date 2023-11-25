#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations cart opinions orders payments products users
python manage.py migrate

python manage.py loaddata populate/*
