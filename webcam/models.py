from django.db import models
from django.utils.timezone import utc
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import uuid


def get_picture_path(picture, filename):
    """
    Generates the path and filename for a picture where
    the file will be saved within the MEDIA_ROOT folder.
    It uses the picture's timestamp for the folder and filename.
    """
    now = datetime.now(utc)
    created_at = now.astimezone(utc)
    pic_date = created_at.strftime('%Y-%m-%d')
    pic_datetime = created_at.strftime('%Y-%m-%d_%H.%M.%S.%f')
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
    # The old label for the whole image
    label = models.ForeignKey(
        'recognition.Label',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True, blank=True,
        related_name="pictures",
        verbose_name="Label",
    )
    # The new labels for the left and right parts of the image
    left_label = models.ForeignKey(
        'recognition.Label',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True, blank=True,
        related_name="left_pictures",
        verbose_name="Left-side label",
    )
    right_label = models.ForeignKey(
        'recognition.Label',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True, blank=True,
        related_name="right_pictures",
        verbose_name="Right-side label",
    )

    class Meta:
        ordering = ['-created_at']
        index_together = [
            ('left_label', 'created_at'),
            ('right_label', 'created_at'),
        ]

    def __str__(self):
        return '{} {}'.format(
            self.image.name.rsplit('.', 1)[-1].upper(),
            self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )

    def image_tag(self):
        return mark_safe('<img src="%s" style="max-width: 100%%" />' % (escape(self.image.url),))

    image_tag.short_description = "Image"
