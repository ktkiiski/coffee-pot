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
        verbose_name="Description"
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
