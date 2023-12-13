#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations cart opinions orders payments products users complaints
python manage.py migrate

python manage.py loaddata populate/*

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
