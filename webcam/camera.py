from .models import Picture
from io import BytesIO
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
        camera.capture(stream, 'jpeg')
        # Save the picture
        return Picture.objects.create(image=stream)
