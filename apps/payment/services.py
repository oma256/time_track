import os
from hashlib import md5
from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone

from apps.payment.models import (
    OrganizationTariffPackage, Tariff, Package, Payment,
)
from utils.datetime import (
    get_payed_tariff_pkg_duration_date,
    get_updated_current_tariff_duration_date,
)


class TariffsQueryServiсe:
    model = Tariff

    @classmethod
    def get_all_tariffs(cls):
        return cls.model.objects.all().order_by('month_price')

    @classmethod
    def get_tariff_by_pk(cls, tariff_pk):
        try:
            return cls.model.objects.get(id=tariff_pk)
        except cls.model.DoesNotExist:
            return None


class PackageQueryService:
    model = Package

    @classmethod
    def get_packages_by_tariff(cls, tariff):

        return cls.model.objects.filter(tariff=tariff).order_by('price')

    @classmethod
    def get_default_tariff_package(cls):
        if cls.model.objects.filter(default=True).exists():
            return cls.model.objects.filter(default=True).first()
        return None

    @classmethod
    def get_package_by_id(cls, tariff_pkg_id):
        try:
            return cls.model.objects.get(id=tariff_pkg_id)
        except cls.model.DoesNotExist:
            return None


class OrganizationTariffPackageQueryService:
    model = OrganizationTariffPackage

    @classmethod
    def create_org_tariff_package(cls, organization):
        package = PackageQueryService.get_default_tariff_package()

        cls.model.objects.create(organization=organization, package=package)

    @classmethod
    def get_tariff_package_by_org(cls, org):
        return cls.model.objects.filter(organization=org).first()

    @classmethod
    def check_org_tariff_pkg_payed(cls, org_tariff_pkg):
        return org_tariff_pkg.duration <= timezone.now().date()

    @classmethod
    def update_current_org_tariff_pkg(cls, payment_id):
        payment = PaymentService.get_payment_by_id(payment_id=payment_id)
        org_tariff_pkg = payment.org_tariff_package

        if payment.org_tariff_package.package.id == payment.tariff_package.id:
            org_tariff_pkg.duration = get_updated_current_tariff_duration_date(
                month_count=payment.tariff_package.month_duration,
                current_tariff=org_tariff_pkg,
            )
            org_tariff_pkg.save(update_fields=['duration'])
        else:
            org_tariff_pkg.package = payment.tariff_package
            org_tariff_pkg.duration = get_payed_tariff_pkg_duration_date(
                month_count=payment.tariff_package.month_duration,
            )
            org_tariff_pkg.save(update_fields=['package', 'duration'])


class PaymentService:
    model = Payment

    @classmethod
    def create_payment(cls, org_tariff, tariff):
        return cls.model.objects.create(
            org_tariff_package=org_tariff, tariff_package=tariff,
        )

    @classmethod
    def update_payment_result(cls, request, pg_order_id):
        update_params = {
            'pg_ps_amount': request.POST.get('pg_amount'),
            'pg_user_phone': request.POST.get('pg_user_phone'),
            'pg_user_contact_email': request.POST.get('pg_user_contact_email'),
            'pg_currency': request.POST.get('pg_currency'),
            'pg_description': request.POST.get('pg_description'),
            'is_paid': True,
        }

        cls.model.objects.filter(id=pg_order_id).update(**update_params)

    @classmethod
    def get_payment_by_id(cls, payment_id):
        try:
            return cls.model.objects.get(id=payment_id)
        except cls.model.DoesNotExist:
            return None


class PayboxService:
    """ Service class for operating with paybox """

    @classmethod
    def generate_paybox_url(cls, payment, org_id):
        paybox_params = {
            'pg_merchant_id': settings.PAYBOX_PROJECT_ID,
            'pg_amount': str(payment.get_total_price),
            'pg_currency': settings.PAYBOX_CURRENCY,
            'pg_payment_id': str(payment.id),
            'pg_order_id': str(payment.id),
            'pg_salt': settings.PAYBOX_SALT,
            'pg_description': f'Заказ № {payment.id}',
            'pg_language': settings.PAYBOX_LANGUAGE,
            'pg_success_url': os.path.join(
                settings.PAYBOX_SUCCESS_URL,
                'organizations',
                str(org_id),
                'tariffs/',
            ),
            'pg_success_url_method': settings.PAYBOX_SUCCESS_URL_METHOD,
            'pg_result_url': settings.PAYBOX_RESULT_URL,
            'secret_key': settings.PAYBOX_SECRET_KEY
        }
        """
            required:
            pg_amount - Сумма платежа в валюте pg_currency (number)
            pg_order_id - Идентификатор платежа в системе продавца.
            Рекомендуется поддерживать уникальность этого поля. (str)
            pg_merchant_id - Идентификатор продавца в PayBox.
            Выдается при подключении. (integer)
            pg_description - Описание товара или услуги.
            Отображается покупателю в процессе платежа.
            pg_salt - string Случайная строка
            pg_sig - string Подпись

            optional fields:
            pg_result_url - string (url) URL для сообщения о результате платежа.
             Вызывается после платежа в случае успеха или неудачи. Если параметр
              не указан, то берется из настроек магазина. Если параметр
              установлен равным пустой строке, то PayBox не сообщает магазину о
              результате платежа.
            pg_refund_url - URL для сообщения об отмене платежа. Вызывается
            после платежа в случае отмены платежа на стороне PayBoxа или ПС.
            Если параметр не указан, то берется из настроек магазина.
            pg_request_method - (string) - Enum:"GET" "POST" "XML" GET, POST
            или XML – метод вызова скриптов магазина Check URL, Result URL,
            Refund URL, для передачи информации от платежного гейта.
            pg_success_url  - string(url, на который отправляется пользователь
            в случае успешного платежа (только для online систем))
            pg_failure_url - url, на который отправляется пользователь в случае
            неуспешного платежа (только для online систем)
            pg_success_url_method - Enum:"GET" "POST" "AUTOGET" "AUTOPOST" GET
            – кнопка, которая сабмитится методом GET. POST – кнопка, которая
            сабмитится методом POST. AUTOGET – 302 редирект. См. Автоматическая
            передача информации, п.1. AUTOPOST – форма, которая автоматически
            сабмитится. См. Автоматическая передача информации, п.2. Если выбран
             метод GET или POST, то страница с подтверждением оплаты
             показывается пользователю на сайте paybox.money, и предлагается
             нажать кнопку, чтобы вернуться на сайт магазина. Если выбран метод
              AUTOGET или AUTOPOST, то страница с подтверждением оплаты не
              показывается пользователю, и пользователь сразу передается
              магазину.
            pg_failure_url_method - Enum:"GET" "POST" "AUTOGET" "AUTOPOST"
            GET – кнопка, которая сабмитится методом GET. POST – кнопка,
            которая сабмитится методом POST. AUTOGET – 302 редирект. См.
            Автоматическая передача информации, п.1. AUTOPOST – форма, которая
            автоматически сабмитится. См. Автоматическая передача информации,
            п.2. Если выбран метод GET или POST, то страница с сообщением о
            неудавшейся оплате показывается пользователю на сайте paybox.money,
            и предлагается нажать кнопку, чтобы вернуться на сайт магазина.
            Если выбран метод AUTOGET или AUTOPOST, то страница с сообщением
            о неудавшейся оплате не показывается пользователю, и пользователь
            сразу передается магазину.
            pg_site_url - URL сайта магазина для показа покупателю ссылки, по
            которой он может вернуться на сайт магазина после создания счета.
            Применяется для offline ПС (наличные).
            pg_lifetime - Время (в секундах) в течение которого платеж должен
            быть завершен, (integer) Default: "86400". Minimum 300 секунд
            (5 минут).
            pg_testing_mode - (integer) Enum:0 1. Создание платежа в тестовом
            режиме.
        """

        paybox_params = dict(sorted(paybox_params.items()))
        pg_sig_gen = cls.generate_sig(paybox_params.values())
        paybox_params['pg_sig'] = pg_sig_gen

        # Пометка на будущее secret_key должен учавстовать в генерации подписи,
        # но передаваться не должен.

        del paybox_params['secret_key']
        url_params = urlencode(paybox_params)

        return f'{settings.PAYBOX_URL}?{url_params}'

    @staticmethod
    def generate_sig(sig_params):
        result = ['payment.php', ';'.join(sig_params)]
        pg_sig = ';'.join(result)
        pg_sig = md5(pg_sig.encode('UTF-8')).hexdigest()

        return pg_sig
