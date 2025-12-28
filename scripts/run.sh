#!/bin/sh

set -e

/py/bin/python manage.py wait_for_db
/py/bin/python manage.py collectstatic --noinput
/py/bin/python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module meshque.wsgi

