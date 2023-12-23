#!/bin/bash

set -e

echo "[INFO] Running django tests: $ python ./app/manage.py test"
python app/manage.py test

echo "[INFO] Launching the django TEST! server: $ python app/manage.py runserver 0.0.0.0:8000"
python app/manage.py runserver 0.0.0.0:8000
