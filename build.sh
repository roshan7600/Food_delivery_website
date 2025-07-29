#!/usr/bin/env bash

# Exit if any command fails
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run collectstatic (for admin panel styles to work)
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
