#!/bin/bash

python manage.py migrate
uvicorn www.asgi:application --reload --port 8000 --host 0.0.0.0