FROM resin/rpi-raspbian:jessie

# switch on systemd init system in container
ENV INITSYSTEM on

# Install Python.
RUN apt-get update \
  && apt-get install -y python3 python3-pip python3-picamera \
  # Remove package lists to free up space
  && rm -rf /var/lib/apt/lists/*

# pip install python deps from requirements.txt
# For caching until requirements.txt changes
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

# Set up configuration for the app
ENV DATABASE_URL sqlite:////data/db.sqlite3

CMD ["bash","start.sh"]
