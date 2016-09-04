from django.core.files.images import ImageFile
from django.utils.timezone import utc
from .models import Picture
from io import BytesIO
from datetime import datetime
import picamera
import time


def take_picture(self):
    """
    Takes a picture with the Rasperry Pi's camera module,
    and saves the file and a Picture model record for it.

    Returns the saved Picture model instance.
    """
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        # Camera warm-up time
        time.sleep(2)
        # Take the picture
        stream = BytesIO()
        camera.capture(stream, 'jpeg', quality=90)
        # Save the picture
        now = datetime.now(utc)
        image_filename = '{}.jpg'.format(now.strftime('%Y-%m-%d_%H.%M.%S'))
        image_file = ImageFile(stream, name=image_filename)
        return Picture.objects.create(image=image_file)
