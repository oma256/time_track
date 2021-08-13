from django.contrib import admin
from django.contrib.gis import admin as geo_admin

from apps.organizations.models import (
    Organization,
    OrganizationSetting,
    WorkTime,
    UserOrganization,
    Feedback,
)
from apps.payment.models import OrganizationTariffPackage


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'admin',
        'parent_org',
    )


@geo_admin.register(OrganizationSetting)
class OrganizationSettingAdmin(geo_admin.ModelAdmin):
    list_display = (
        'id',
        'organization',
        'start_time',
        'end_time',
        'non_fined_minute',
        'location',
        'qr_code',
        'radius',
    )


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_organization',
        'start_time',
        'end_time',
        'is_late',
    )
    ordering = ('start_time',)


@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'position',
        'organization',
        'start_time',
        'end_time',
        'non_fined_minute',
        'is_checked',
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('phone', 'finished')


@admin.register(OrganizationTariffPackage)
class OrganizationTariffPackageAdmin(admin.ModelAdmin):
    list_display = ('organization', 'package', 'duration')
