#!/bin/sh
celery -A hulahoop worker -B -l info -Q celery -n celery@local --max-tasks-per-child 100 --autoscale=8,1