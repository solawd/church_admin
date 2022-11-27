#!/bin/sh
# This file can be used to initialize a freshly deployed system
# It runs migrations and uses the initadmin management command to setup a default superuser
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py initadmin