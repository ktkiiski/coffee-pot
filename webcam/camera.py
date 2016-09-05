from django.core.files.images import ImageFile
from django.utils.timezone import utc
from .models import Picture
from io import BytesIO
from datetime import datetime
import scipy.misc
import time


def capture_image():
    stream = BytesIO()
    try:
        import picamera
    except Exception:
        # Cannot import picamera, so let's use a dummy image instead
        scipy.misc.imsave(stream, scipy.misc.face(), 'jpeg')
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

    Returns the saved Picture model instance.
    """
    stream = capture_image()
    # Save the picture
    now = datetime.now(utc)
    image_filename = '{}.jpg'.format(now.strftime('%Y-%m-%d_%H.%M.%S'))
    image_file = ImageFile(stream, name=image_filename)
    return Picture.objects.create(image=image_file)
