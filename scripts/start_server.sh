#!/bin/bash
python manage.py migrate &&
python manage.py collectstatic --noinput &&
python manage.py shell < initial_script/populate_plans.py
gunicorn --bind 0.0.0.0:8000 saas_project.wsgi:application