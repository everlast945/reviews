#!/bin/bash

gunicorn setting.wsgi:app \
--chdir ./reviews \
--bind 0.0.0.0:8000 \
--workers 5 \
--timeout 120
