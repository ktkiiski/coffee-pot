# Coffee Watch

## To read

- [Getting Started with Raspberry Pi 1 or ZERO and Node.js](https://docs.resin.io/raspberrypi/nodejs/getting-started/)
- [picamera documentation](http://picamera.readthedocs.org/en/release-1.8/)


## Setup

Clone this repository:

```bash
git clone git@github.com:ktkiiski/coffee-watch.git
cd coffee-watch
```

To run Python scripts locally, [create a virtualenv](http://virtualenvwrapper.readthedocs.io/en/latest/) for them. Run these in your local repository directory:

```bash
mkvirtualenv -a . --python=python3.5 coffee-watch
pip install -r requirements.txt
```

On the following terminal sessions, run the following command to re-activate the virtualenv and switching to the working directory:

```bash
workon coffee-watch
```

## Repository structure

Here's the function of different folders:

- `barista`: The Django-powered HTTP server project folder. It contains a WSGI server application.
- `coffeestatus`: The Django "app" that is run by the `barista` project. It handles the command requests made from Slack.
- `webcam`: The Django "app" Python module containing database models for storing webcam photos, as logic for taking them.
- `examples`: Contains some extra files for development purposes. They are not used by the final app.

## Running the HTTP server

The Rasperry Pi runs a HTTP server, implemented with [Django](https://www.djangoproject.com/) for processing commands sent from Slack.

Before you run the server for the first time, you should initialize the SQLite database:

```bash
python manage.py migrate
```

This will run database migrations, creating a file `db.sqlite3` to the root of the repository (excluded from version control).

You can then start the server:

```bash
python manage.py runserver
```

## Configuration

The app can be configured with environment variables:

Environment variable | Description
---------------------|------------
`MEDIA_PATH` | The full path under which the Django will store files, especially the captured pictures. This already has a meaningful default in both local development and in the [Dockerfile](./Dockerfile.template)
`DATABASE_URL` | The database URI that configures where the SQlite database file is stored. E.g. `sqlite:////data/db.sqlite3`. This already has a meaningful default in both local development and in the [Dockerfile](./Dockerfile.template)
`SLACK_COMMAND_TOKEN` | The token that is required by Slack command requests. If not defined, then no token validation is done.
`SNAPSHOT_SCHEDULE_TIMEZONE` | The timezone in which the snapshot scheduling is set up. E.g. `Europe/Helsinki`. Defaults to `UTC`
`SNAPSHOT_SCHEDULE_INTERVAL` | The number of minutes between scheduled snapshots
`SNAPSHOT_SCHEDULE_START_TIME` | The time of the day when the scheduled snapshots begin, e.g. `07:00`
`SNAPSHOT_SCHEDULE_END_TIME` | The time of the day when the scheduled snapshots end, e.g. `17:00`
`SNAPSHOT_SCHEDULE_WEEKDAYS` | Comma separated list of integers, describing on which week days the scheduled snapshots are taken. Monday is `1`, Tuesday is `2`, and so on. E.g. `1,2,3,4,5`
