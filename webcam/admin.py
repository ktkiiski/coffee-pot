from django.contrib import admin
from webcam.models import Picture


@admin.register(Picture)
class AuthorAdmin(admin.ModelAdmin):
    fields = (
        'created_at',
        'image_tag',
        'image',
        'width',
        'height',
    )
    readonly_fields = (
        'created_at',
        'image_tag',
        'width',
        'height',
    )
