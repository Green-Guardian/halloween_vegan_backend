#!/bin/bash

set -e

echo "[INFO] Generating static content"
python app/manage.py collectstatic --noinput

#echo "[INFO] Running django tests: $ python ./app/manage.py test"
#python app/manage.py test

#echo "[INFO] Running django oauth2_provider migration: $ app/manage.py migrate oauth2_provider"
#python app/manage.py migrate oauth2_provider


echo "[INFO] Launching the django server: $ daphne -b 0.0.0.0 -p 8000 app.halloween_vegan_backend.asgi:application"
daphne -b 0.0.0.0 -p 8000 app.halloween_vegan_backend.asgi:application
