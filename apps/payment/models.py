import decimal

from django.db import models
from django.utils import timezone

from apps.organizations.models import Organization
from utils.datetime import get_default_duration_date


class Tariff(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    month_price = models.DecimalField(
        verbose_name='Цена за 1 месяц', max_digits=10, decimal_places=0,
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class Package(models.Model):
    price = models.DecimalField(
        verbose_name='Цена', max_digits=10, decimal_places=0,
    )
    discount = models.PositiveSmallIntegerField(
        verbose_name='Скидка (%)', null=True, blank=True
    )
    month_duration = models.PositiveSmallIntegerField(
        verbose_name='Период (в месяцах)',
    )
    tariff = models.ForeignKey(
        to='Tariff', on_delete=models.SET_NULL, null=True,
        related_name='packages',
    )
    default = models.BooleanField('Пакет по умолчанию', default=False)

    class Meta:
        verbose_name = 'Тарифный пакет'
        verbose_name_plural = 'Тарифные пакеты'

    def __str__(self):
        return f'Пакет (Тариф: {self.tariff.name}, скидка: {self.discount})'

    @property
    def get_discount(self):
        if self.discount:
            return round(self.price * decimal.Decimal(1 - self.discount / 100))
        return None


class OrganizationTariffPackage(models.Model):
    organization = models.ForeignKey(
        to=Organization, on_delete=models.SET_NULL, related_name='tariffs',
        null=True,
    )
    package = models.ForeignKey(
        to=Package, on_delete=models.SET_NULL, related_name='organizations',
        null=True,
    )
    duration = models.DateField(
        verbose_name='Срок действия до', default=get_default_duration_date,
    )

    class Meta:
        verbose_name = 'Тариф организации'
        verbose_name_plural = 'Тарифы организаций'

    def __str__(self):
        return f'{self.organization.name} -> {self.package.tariff.name}'

    @property
    def duration_days_count(self):
        duration_days = (self.duration - timezone.now().date()).days

        if duration_days < 1:
            return 0
        return duration_days


class Payment(models.Model):
    org_tariff_package = models.ForeignKey(
        to=OrganizationTariffPackage, on_delete=models.SET_NULL,
        related_name='org_payments', null=True,
    )
    tariff_package = models.ForeignKey(
        to=Package, on_delete=models.SET_NULL,
        related_name='package_payments', null=True,
    )
    pg_user_phone = models.CharField(
        verbose_name='Указанный номер тел. в PayBox', max_length=13, null=True,
        blank=True,
    )
    pg_user_contact_email = models.EmailField(
        verbose_name='Указанная почта в PayBox', null=True, blank=True,
    )
    pg_ps_amount = models.CharField(
        verbose_name='Сумма оплаты', max_length=255, null=True, blank=True,
    )
    pg_currency = models.CharField(
        verbose_name='Валюта', max_length=255, null=True, blank=True,
    )
    pg_description = models.CharField(
        verbose_name='Описание', max_length=255, null=True, blank=True,
    )
    is_paid = models.BooleanField(verbose_name='Оплачен', default=False)
    date_time = models.DateTimeField(verbose_name='Дата/Время', auto_now=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж #{self.id}'

    @property
    def get_total_price(self):
        tariff_pkg_discount = self.tariff_package.discount
        if self.tariff_package.discount:
            return round(
                self.tariff_package.price * decimal.Decimal(
                    1 - tariff_pkg_discount / 100
                )
            )
        return self.tariff_package.price
