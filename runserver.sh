#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic
python manage.py initadmin
python manage.py runserver 0.0.0.0:8080