from django.db import models
from django.utils.timezone import utc
import uuid


def get_picture_path(picture, filename):
    """
    Generates the path and filename for a picture where
    the file will be saved within the MEDIA_ROOT folder.
    It uses the picture's timestamp for the folder and filename.
    """
    created_at = picture.created_at.astimezone(utc)
    pic_date = created_at.strftime('%Y-%m-%d')
    pic_datetime = created_at.strftime('%Y-%m-%d_%H.%M.%S')
    extension = filename.rsplit(".", 1)[-1]
    return 'snapshots/{}/{}.{}'.format(pic_date, pic_datetime, extension)


class Picture(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False,
        verbose_name="Unique identifier",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation date/time",
        db_index=True,
    )
    image = models.ImageField(
        upload_to=get_picture_path,
        width_field='width',
        height_field='height',
        verbose_name="Camera snapshot image",
    )
    width = models.PositiveIntegerField(
        verbose_name="Image width",
    )
    height = models.PositiveIntegerField(
        verbose_name="Image height",
    )
