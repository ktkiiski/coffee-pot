from django.db import models
from django.utils.timezone import utc
import uuid


def get_picture_path(picture, filename):
    created_at = picture.created_at.astimezone(utc)
    pic_date = created_at.strftime('%Y-%m-%d')
    pic_datetime = created_at.strftime('%Y-%m-%d %H.%M.%S')
    return 'uploads/{}/{} {}'.format(pic_date, pic_datetime, filename)


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
