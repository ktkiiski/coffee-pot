from datetime import datetime, time, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from webcam.models import Picture
from webcam.camera import take_picture
from coffeestatus.watch import check_fresh_coffee
from recognition.prediction import predict_picture_labels
from pytz import timezone


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
        parser.add_argument(
            '--notify',
            action='store_true',
            dest='notify',
            default=False,
            help='Check if there is now fresh coffee and notify Slack',
        )
        parser.add_argument(
            '--no-predict',
            action='store_true',
            dest='no_predict',
            default=False,
            help='Do not attempt to predict the picture labels. This also disables Slack notifications.',
        )

    def handle(self, *args, scheduled=False, no_predict=False, notify=False, **options):
        if scheduled and not self.should_take_picture():
            # Should not take a picture
            return

        pic = take_picture()
        self.stdout.write(
            self.style.SUCCESS('Successfully captured a picture: {}'.format(pic.image.url))
        )

        if not no_predict:
            predict_picture_labels(pic)
            self.stdout.write(
                'Left label: "{}" ({}) / Right label: "{}" ({})'.format(
                    pic.recognized_left_label_id, pic.recognized_left_probability,
                    pic.recognized_right_label_id, pic.recognized_right_probability,
                )
            )
            fresh_coffee = check_fresh_coffee(pic)
            if fresh_coffee:
                self.stdout.write(self.style.SUCCESS(fresh_coffee))
                if notify:
                    self.stdout.write(
                        "TODO: Check for fresh coffee and notify Slack!"
                    )

    def should_take_picture(self):
        """
        Check if the current timestamp is within the scheduled ranges.
        """
        tz = timezone(settings.SNAPSHOT_SCHEDULE_TIMEZONE)
        now = datetime.now(tz)
        weekdays = set(int(d) for d in settings.SNAPSHOT_SCHEDULE_WEEKDAYS.split(','))
        start_hour, start_minute = [
            int(c) for c in settings.SNAPSHOT_SCHEDULE_START_TIME.split(':')
        ]
        end_hour, end_minute = [int(c) for c in settings.SNAPSHOT_SCHEDULE_END_TIME.split(':')]
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)
        now_time = now.time()
        now_weekday = now.isoweekday()
        interval_mins = settings.SNAPSHOT_SCHEDULE_INTERVAL
        interval = timedelta(minutes=settings.SNAPSHOT_SCHEDULE_INTERVAL) - timedelta(seconds=10)
        try:
            min_now = Picture.objects.latest('created_at').created_at.astimezone(tz) + interval
        except Picture.DoesNotExist:
            min_now = datetime(2000, 1, 1, tzinfo=tz)
        if now_weekday not in weekdays:
            self.stdout.write('Capturing disabled this week day')
            return False
        if not start_time <= now_time <= end_time:
            self.stdout.write('Capturing disabled this time of the day')
            return False
        if now < min_now:
            self.stdout.write('Not enough time (%d mins) passed since the latest capture' % interval_mins)
            return False
        return True
