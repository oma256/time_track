import datetime
import io
import json
import re
from abc import ABC

import pyqrcode
import pytz
from django.core.files import File
from django.template.loader import render_to_string
from django.utils import timezone


class BaseQueryService(ABC):

    @classmethod
    def parse_data(cls, data: bytes) -> dict:
        result = json.loads(data.decode())

        return result

    @staticmethod
    def create_qr_code(instance):
        qr_content = f'{instance.id}' \
                     f'?{instance.org_settings.location.x}' \
                     f'?{instance.org_settings.location.y}' \
                     f'?{instance.org_settings.radius}'
        qr_code = pyqrcode.create(content=qr_content, encoding='utf-8')

        with io.BytesIO() as _bytes:
            qr_code.svg(_bytes, scale=4)
            _bytes.seek(0)
            instance.org_settings.qr_code.save(
                f'{qr_content}_qr.svg', content=File(_bytes), save=True
            )
            instance.save()

    @staticmethod
    def get_html_template(request, tmp_name, data):
        return render_to_string(template_name=tmp_name,
                                context=data,
                                request=request)

    @staticmethod
    def generate_time(data: dict) -> dict:
        if data.get('begin_hour'):
            data['start_time'] = datetime.time(data.pop('begin_hour'),
                                               data.pop('begin_min'))
            data['end_time'] = datetime.time(data.pop('end_hour'),
                                             data.pop('end_min'))

        return data

    @staticmethod
    def clean_phone(data: dict) -> dict:
        phone = data.pop('phone_number')
        data['phone_number'] = '+' + re.sub(r"\D", "", str(phone))

        return data

    @staticmethod
    def get_last_month_date_range():
        current_date = timezone.now().date() + datetime.timedelta(days=1)
        month_ago_date = current_date - datetime.timedelta(days=31)

        return month_ago_date, current_date

    @staticmethod
    def convert_to_localtime(utctime):
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())

        return localtz

    @classmethod
    def convert_str_to_date_format(cls, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
