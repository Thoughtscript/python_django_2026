#!/usr/bin/env bash

echo "Preparing migrations..." && echo "Waiting 25 seconds for DB to complete initializing..." && sleep 25 && echo "Migrating DB and running server" && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py seed &

echo "Waiting 25 seconds for DB initializations and migrations to complete..." && sleep 25 && echo "Waiting 5-10 seconds to launch web app..." && sleep 10 && gunicorn -c gunicorn.conf.py djangoexample.asgi:application & 

wait