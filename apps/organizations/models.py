import datetime

from django.contrib.gis.db.models import PointField
from django.db import models

from utils.upload_avatar_file import upload_instance
from utils.user_phone_number_regex import phone_regex


class Organization(models.Model):
    name = models.CharField('Название', max_length=255, null=True)
    parent_org = models.ForeignKey(to='self',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    admin = models.ForeignKey(to='users.User',
                              on_delete=models.SET_NULL,
                              related_name='admin_organization',
                              null=True)
    is_department = models.BooleanField('Отдел', default=False)

    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организаций'

    def __str__(self):
        if self.parent_org:
            return f'{self.parent_org.name} => {self.name}'
        return self.name


class OrganizationSetting(models.Model):
    organization = models.OneToOneField(to='Organization',
                                        on_delete=models.CASCADE,
                                        related_name='org_settings')
    start_time = models.TimeField('Время начала', default=datetime.time(9, 00))
    end_time = models.TimeField('Время окончания', default=datetime.time(18, 00))
    non_fined_minute = models.PositiveSmallIntegerField('Не штрафуемые минуты',
                                                        default=10)
    location = PointField('Локация', null=True, blank=True)
    qr_code = models.FileField('QR-код',
                               upload_to=upload_instance,
                               null=True, blank=True)
    radius = models.PositiveSmallIntegerField('Радиус', default=100)

    class Meta:
        verbose_name = 'Настройка организации'
        verbose_name_plural = 'Настройки организаций'

    def __str__(self):
        return self.organization.__str__()


class WorkTime(models.Model):
    user_organization = models.ForeignKey(to='UserOrganization',
                                          on_delete=models.SET_NULL,
                                          related_name='work_times',
                                          null=True)
    start_time = models.DateTimeField('Время входа')
    end_time = models.DateTimeField('Время выхода', null=True)
    is_late = models.BooleanField('Опоздал', default=False)

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

    def __str__(self):
        return f'Время: {self.start_time} - {self.end_time}'


class UserOrganization(models.Model):
    user = models.ForeignKey(to='users.User',
                             on_delete=models.SET_NULL,
                             related_name='user_organizations',
                             null=True)
    position = models.CharField('Должность', max_length=255, null=True)
    organization = models.ForeignKey(to='Organization',
                                     on_delete=models.SET_NULL,
                                     null=True)
    is_checked = models.BooleanField('Отмечен', default=False)
    start_time = models.TimeField('Время начала', default=datetime.time(9, 00))
    end_time = models.TimeField('Время окончания',
                                default=datetime.time(18, 00))
    non_fined_minute = models.PositiveSmallIntegerField('Не штрафуемые минуты',
                                                        default=10)

    class Meta:
        verbose_name = 'Организация пользователя'
        verbose_name_plural = 'Организаций пользователей'

    def __str__(self):
        return f'{self.user} - {self.organization}'


class Feedback(models.Model):
    phone = models.CharField(
        verbose_name='Номер телефона', max_length=15, validators=[phone_regex],
    )
    finished = models.BooleanField(verbose_name='Обработан', default=False)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'

    def __str__(self):
        return self.phone
