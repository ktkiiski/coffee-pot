# Coffee Pot

![Coffee Pot](examples/snapshots/2016-10-13_05.54.10.077663.jpg)

The awesome webcam bot that watches your coffee pots and can be integrated with Slack.
It is designed to be run on a Raspberry Pi with a camera module, and running on [Resin.io](resin.io) OS.

## Local development

### Clone the repository

Make a local clone of this repository:

```bash
git clone git@github.com:ktkiiski/coffee-pot.git
cd coffee-pot
```

### Python 3 virtualenv

To run Python scripts locally, [create a virtualenv](http://virtualenvwrapper.readthedocs.io/en/latest/) for them. You must use **Python 3**. Run these in your local repository directory:

```bash
mkvirtualenv -a . --python=python3.5 coffee-pot
pip install -r requirements.txt
```

On the following terminal sessions, run the following command to re-activate the virtualenv and switching to the working directory:

```bash
workon coffee-pot
```

### Create Amazon S3 bundle

In order to work, you need a Amazon S3 bundle to which the captured images will be loaded. You also need to create an access key and a secret that allows uploading files to your bucket.

### Configuration

You then need to configure some environment variables.
Your virtualenv post-activate hook is a nice place to do this:

```bash
nano $VIRTUALENVWRAPPER_HOOK_DIR/postactivate
```

Then add this to the file:

```bash
# Your Slack webhook URL. Required if you want to make Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
# Your AWS access key used to access the storage buckets.
export AWS_ACCESS_KEY_ID="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Your AWS secret access key used to access the storage buckets.
export AWS_SECRET_ACCESS_KEY="abcdefghijklmnopqrstuvwxyz1234567890"
# The region to connect to when storing files.
export AWS_REGION="eu-central-1"
# The S3 bucket used to store uploaded files.
export AWS_S3_BUCKET_NAME="coffee-pot"
# A prefix to add to the start of all uploaded files. Defaults to "media".
# Allows sharing the same bucket with multiple environments.
export AWS_S3_KEY_PREFIX="__dev_media"
```

**For all configuration options, see [Environment variables](#environment-variables) below!**

Then re-activate your virtualenv:

```bash
deactivate && workon coffee-pot
```

## Repository structure

Here's the function of different folders:

- `barista`: The Django-powered HTTP server project folder. It contains a WSGI server application.
- `coffeestatus`: The Django "app" that is run by the `barista` project. It handles the command requests made from Slack.
- `webcam`: The Django "app" Python module containing database models for storing webcam photos, as logic for taking them.
- `examples`: Contains some example webcam snapshot files for local development, when an actual Raspberry Pi camera module is not available. When taking a snapshot, one of these images are chosen randomly.

## Running the HTTP server

The app runs a HTTP server, implemented with [Django](https://www.djangoproject.com/) for processing commands sent from Slack.

Before you run the server for the first time, you should initialize the SQLite database:

```bash
python manage.py migrate
python manage.py loaddata labels
```

This will run database migrations, creating a file `db.sqlite3` to the root of the repository (excluded from version control).
The second line loads the default labels.

You can then start the server:

```bash
python manage.py runserver
```

## Capturing pictures

You can capture images by using the `capture` Django command:

```bash
python manage.py capture
```

You can capture conditionally only if the current time matches the configured schedules:

```bash
python manage.py capture --scheduled
```

If there is fresh coffee, you may also notify Slack, according to the configuration. Note that this only works if the `SLACK_WEBHOOK_URL` environment variable is configured.

```bash
python manage.py capture --notify
```

Label prediction is done by default. You can disable it if you wish (but this also disables Slack notifications):

```bash
python manage.py capture --no-predict
```

More information:

```bash
python manage.py help capture
```

## Environment variables

The app **must** be configured with the following required environment variables:

Environment variable | Description
---------------------|------------
`AWS_ACCESS_KEY_ID` | Your AWS access key used to access the storage buckets.
`AWS_SECRET_ACCESS_KEY` | Your AWS secret access key used to access the storage buckets.
`AWS_REGION` | The region to connect to when storing files.
`AWS_S3_BUCKET_NAME` | The S3 bucket used to store uploaded files.

The _may_ be also configured with the following optional environment variables:

Environment variable | Description
---------------------|------------
`AWS_S3_KEY_PREFIX` | A prefix to add to the start of all uploaded files. Defaults to `media`. Allows sharing the same bucket with multiple environments.
`AWS_S3_KEY_PREFIX_STATIC` | A prefix to add to the start of all static files when stored in Amazon S3 (in production). Defaults to `static`.
`DATABASE_URL` | The database URI that configures where the SQlite database file is stored. E.g. `sqlite:////data/db.sqlite3`. This already has a meaningful default in both local development and in the [Dockerfile](./Dockerfile.template)
`SLACK_WEBHOOK_URL` | The [Slack incoming webhook URL](https://api.slack.com/incoming-webhooks) to which Slack notifications are made. If not enabled then Slack notifications will be disabled.
`SLACK_COMMAND_TOKEN` | The token that is required by Slack command requests. If not defined, then no token validation is done.
`SNAPSHOT_SCHEDULE_TIMEZONE` | The timezone in which the snapshot scheduling is set up. E.g. `Europe/Helsinki`. Defaults to `UTC`
`SNAPSHOT_SCHEDULE_INTERVAL` | The number of minutes between scheduled snapshots. Defaults to `1`
`SNAPSHOT_SCHEDULE_START_TIME` | The time of the day when the scheduled snapshots begin, e.g. `07:00`. Defaults to `00:00`
`SNAPSHOT_SCHEDULE_END_TIME` | The time of the day when the scheduled snapshots end, e.g. `17:00`. Defaults to `23:59`
`SNAPSHOT_SCHEDULE_WEEKDAYS` | Comma separated list of integers, describing on which week days the scheduled snapshots are taken. Monday is `1`, Tuesday is `2`, and so on. E.g. `1,2,3,4,5`. Defaults to every day.

## To read

- [Getting Started with Raspberry Pi 1 or ZERO and Node.js](https://docs.resin.io/raspberrypi/nodejs/getting-started/)
- [picamera documentation](http://picamera.readthedocs.org/en/release-1.8/)
