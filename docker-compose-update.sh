#!/bin/bash
cd /usr/src/timtec
npm install
bower --allow-root install
pip install --no-cache-dir ipdb
python /usr/src/timtec/manage.py migrate
python /usr/src/timtec/manage.py runserver 0.0.0.0:8000
