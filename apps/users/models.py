import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.users.managers import UserManager
from utils.user_phone_number_regex import phone_regex


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(
        verbose_name='Отчество', max_length=255, blank=True, null=True,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона', validators=[phone_regex], max_length=20,
        unique=True,
    )
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    is_staff = models.BooleanField(verbose_name='Сотрудник', default=False)
    date_joined = models.DateTimeField(
        verbose_name='Зарегестрирован', default=timezone.now,
    )

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        full_name = ''

        if self.last_name:
            full_name += self.last_name
        if self.first_name:
            full_name += f' {self.first_name}'
        if self.middle_name:
            full_name += f' {self.middle_name}'

        return full_name

    @property
    def get_first_name(self):
        return self.first_name


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
