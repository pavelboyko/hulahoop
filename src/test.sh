#!/bin/sh
coverage run --source='.' ./manage.py test && coverage html