#!/bin/bash

set -e

source /home/aikon/app/config/.env

# wait 2sec for postgres to start
sleep 2

/home/aikon/venv/bin/python /home/aikon/app/manage.py migrate

/home/aikon/venv/bin/python /home/aikon/create_superuser.py

## Create superuser if it doesn't exist
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('$db_user', '$CONTACT_MAIL', '$POSTGRES_PASSWORD')" | "$APP_ROOT"/venv/bin/python "$APP_ROOT"/app/manage.py shell
#/home/aikon/venv/bin/python /home/aikon/app/manage.py shell << END
#  from django.contrib.auth import get_user_model
#  User = get_user_model()
#  if not User.objects.filter(username='${POSTGRES_USER}').exists():
#      User.objects.create_superuser('${POSTGRES_USER}', '${CONTACT_MAIL}', '${POSTGRES_PASSWORD}')
#      print('Superuser created.')
#  else:
#      print('Superuser already exists.')
#END
#/home/aikon/venv/bin/python /home/aikon/app/manage.py createsuperuser --username="$POSTGRES_USER" --email="$CONTACT_MAIL"

/home/aikon/venv/bin/python /home/aikon/app/manage.py collectstatic --noinput
