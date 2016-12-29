from django.conf import settings
from django.core.files.images import ImageFile
from django.utils.timezone import utc
from .models import Picture
from io import BytesIO
from datetime import datetime
import time
import random
import os.path
import logging

logger = logging.getLogger(__name__)


def capture_image():
    stream = BytesIO()
    try:
        import picamera
    except Exception:
        # Cannot import picamera, so let's use a dummy image instead
        pic_folder = os.path.join(settings.BASE_DIR, "examples/snapshots")
        img_path = os.path.join(pic_folder, random.choice(os.listdir(pic_folder)))
        with open(img_path, 'rb') as img:
            stream.write(img.read())
    else:
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            # Camera warm-up time
            time.sleep(2)
            # Take the picture
            camera.capture(stream, 'jpeg', quality=90)
    return stream


def take_picture():
    """
    Takes a picture with the Rasperry Pi's camera module,
    and saves the file and a Picture model record for it.

    It then tries to recognize the labels for the image.

    Returns the saved Picture model instance.
    """
    stream = capture_image()
    # Save the picture
    now = datetime.now(utc)
    image_filename = '{}.jpg'.format(now.strftime('%Y-%m-%d_%H.%M.%S'))
    image_file = ImageFile(stream, name=image_filename)
    return Picture.objects.create(image=image_file)
