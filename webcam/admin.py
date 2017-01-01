from django.contrib import admin
from webcam.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    fields = (
        'created_at',
        'image_tag',
        'image',
        'width',
        'height',
        'left_label',
        'right_label',
        'recognized_left_label',
        'recognized_left_probability',
        'recognized_right_label',
        'recognized_right_probability',
    )
    readonly_fields = (
        'created_at',
        'image_tag',
        'width',
        'height',
    )
    list_display = (
        'created_at',
        'description',
    )
