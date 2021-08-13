from django.utils import timezone


def get_default_duration_date():
    return timezone.now().date() + timezone.timedelta(days=15)


def get_payed_tariff_pkg_duration_date(month_count):
    return timezone.now().date() + timezone.timedelta(days=30*month_count)


def get_updated_current_tariff_duration_date(month_count, current_tariff):
    if current_tariff.duration < timezone.now().date():
        return timezone.now().date() + timezone.timedelta(days=30*month_count)
    return current_tariff.duration + timezone.timedelta(days=30*month_count)
