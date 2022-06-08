#!/bin/sh
coverage run --source='.' ./manage.py test --keepdb && coverage report && coverage html