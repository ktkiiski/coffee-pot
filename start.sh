#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate

# Prepare log files and start outputting logs to stdout
mkdir -p /srv/logs
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/cronjobs.log
tail -n 0 -f /srv/logs/*.log &

# Dump the environment variables to a file, for loading to cron
env > envdump.txt

# Start Gunicorn processes
echo "Starting Gunicorn..."
exec gunicorn coffeewatch.wsgi:application \
    --name coffeewatch \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"
