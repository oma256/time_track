from django.contrib import admin

from apps.api.models import VersionControl


@admin.register(VersionControl)
class VersionControlAdmin(admin.ModelAdmin):
    list_display = ('version', 'force_update')
