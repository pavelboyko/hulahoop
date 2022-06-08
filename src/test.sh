#!/bin/sh
coverage run --source='.' ./manage.py test --keepdb && \
coverage report --skip-covered --omit=hulahoop/* && \
coverage html --skip-covered --omit=hulahoop/*