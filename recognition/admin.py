from django.contrib import admin
from recognition.models import Label, LabelCombination


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
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


@admin.register(LabelCombination)
class LabelCombinationAdmin(admin.ModelAdmin):
    fields = (
        'primary_label',
        'secondary_label',
        'description_template',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
