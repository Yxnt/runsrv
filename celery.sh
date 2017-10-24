#!/bin/sh
venv/bin/celery -A runserver.celery worker -l INFO -B
