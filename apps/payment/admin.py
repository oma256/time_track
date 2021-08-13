from django.contrib import admin

from apps.payment.models import Tariff, Package, Payment


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'month_price')


@admin.register(Package)
class PackageInline(admin.ModelAdmin):
    list_display = ('price', 'discount', 'month_duration', 'tariff', 'default')


@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = (
        'org_tariff_package', 'tariff_package', 'pg_user_phone', 'pg_ps_amount',
        'pg_user_contact_email', 'pg_currency', 'pg_description', 'date_time',
        'is_paid',
    )
    ordering = ('date_time',)
