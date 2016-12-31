from uuid import uuid1
from django.db import models


class Label(models.Model):

    id = models.SlugField(
        primary_key=True,
        max_length=64,
        verbose_name="Label",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation date/time",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last update date/time",
    )
    title = models.CharField(
        verbose_name="Title",
        max_length=128,
    )
    description = models.TextField(
        verbose_name="Description",
    )
    order = models.PositiveIntegerField(
        verbose_name="Ordering",
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class LabelCombination(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid1,
        editable=False,
        verbose_name="Unique identifier",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation date/time",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last update date/time",
    )
    left_label = models.ForeignKey(
        'recognition.Label',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="+",
        verbose_name="Left-side label",
    )
    right_label = models.ForeignKey(
        'recognition.Label',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="+",
        verbose_name="Right-side label",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="What these two labels would be described together?",
    )

    def __str__(self):
        return "{} & {}: {}".format(
            self.left_label, self.right_label, self.description
        )

    class Meta:
        unique_together = [
            ('left_label', 'right_label'),
        ]
        ordering = [
            'left_label__order',
            'right_label__order',
        ]
