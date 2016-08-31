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
