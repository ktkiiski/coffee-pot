from django.contrib import admin
from recognition.models import Label


@admin.register(Label)
class AuthorAdmin(admin.ModelAdmin):
    fields = (
        'id',
        'order',
        'title',
        'description',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
