from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from webcam.models import Picture
from webcam.camera import take_picture
from pytz import timezone
from datetime import datetime, time, timedelta


class Command(BaseCommand):
    help = 'Captures an image from the camera and saves it'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scheduled',
            action='store_true',
            dest='scheduled',
            default=False,
            help='Capture an image only if the current time matches the scheduling settings',
        )

    def handle(self, *args, **options):
        if options['scheduled']:
            # Check if the current timestamp is within the scheduled ranges
            tz = timezone(settings.SNAPSHOT_SCHEDULE_TIMEZONE)
            now = datetime.now(tz)
            weekdays = set(int(d) for d in settings.SNAPSHOT_SCHEDULE_WEEKDAYS.split(','))
            start_hour, start_minute = [int(c) for c in settings.SNAPSHOT_SCHEDULE_START_TIME.split(':')]
            end_hour, end_minute = [int(c) for c in settings.SNAPSHOT_SCHEDULE_END_TIME.split(':')]
            start_time = time(start_hour, start_minute)
            end_time = time(end_hour, end_minute)
            now_time = now.time()
            now_weekday = now.isoweekday()
            interval_mins = settings.SNAPSHOT_SCHEDULE_INTERVAL
            interval = timedelta(minutes=settings.SNAPSHOT_SCHEDULE_INTERVAL) - timedelta(seconds=1)
            try:
                min_now = Picture.objects.latest('created_at').created_at.astimezone(tz) + interval
            except Picture.DoesNotExist:
                min_now = datetime(2000, 1, 1, tzinfo=tz)
            if now_weekday not in weekdays:
                self.stdout.write('Capturing disabled this week day')
                return
            if not (start_time <= now_time <= end_time):
                self.stdout.write('Capturing disabled this time of the day')
                return
            if now < min_now:
                self.stdout.write('Not enough time (%d mins) passed since the latest capture' % interval_mins)
                return

        pic = take_picture()
        self.stdout.write(self.style.SUCCESS('Successfully captured a picture (ID: %s)' % pic.id))
