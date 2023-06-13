#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:8080 "app:create_app()"