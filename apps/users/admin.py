from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


AdminSite.site_header = 'Администрирование Work Time'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'last_name', 'first_name', 'middle_name', 'phone_number',
    )
    search_fields = ('last_name', 'first_name', 'middle_name', 'phone_number')
    list_filter = ()
    ordering = []
    fieldsets = (
        (None, {
            'fields': (
                'last_name',
                'first_name',
                'middle_name',
                'phone_number',
                'password',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_superuser',
                'is_staff',
                'is_active',
                'groups',
            )
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
