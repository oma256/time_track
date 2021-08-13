from django.contrib.auth import authenticate
from django.forms import (
    Form, ValidationError, CharField, TextInput, PasswordInput,
)
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from utils.user_phone_number_regex import clean_phone


class UserLoginForm(Form):
    phone_number = CharField(
        max_length=20,
        required=True,
        error_messages={'required': _('укажите номер телефона')},
        widget=TextInput(
            attrs={
                'placeholder': _('Номер телефона'),
                'autocomplete': 'off',
                'id': 'phone_id',
            }
        )
    )
    password = CharField(
        max_length=128,
        required=True,
        error_messages={'required': _('укажите пароль')},
        widget=PasswordInput(
            attrs={
                'placeholder': 'Введите пароль',
                'autocomplete': 'off',
            }
        )
    )

    def clean_phone_number(self):
        _phone = clean_phone(self.cleaned_data.get('phone_number'))
        _user = User.objects.filter(phone_number=_phone).exists()

        if not _user:
            raise ValidationError(_('неверный номер телефона'))

        return _phone

    def clean_password(self):
        _phone = clean_phone(self.cleaned_data.get('phone_number'))
        _pass = self.cleaned_data.get('password')
        _user = authenticate(phone_number=_phone, password=_pass)

        if not _user:
            raise ValidationError(_('неверный пароль'))

        return _pass


class UserRegistrationForm(Form):
    phone_number = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('укажите номер телефона')},
        widget=TextInput(
            attrs={
                'placeholder': 'Номер телефона',
                'autocomplete': 'off',
                'readonly': True,
            }
        ),
    )
    password = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('укажите пароль')},
        widget=TextInput(
            attrs={
                'placeholder': 'Пароль',
                'autocomplete': 'off',
                'type': 'password',
            }
        ),
    )
    password2 = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('повторите пароль')},
        widget=TextInput(
            attrs={
                'placeholder': 'Повторите пароль',
                'autocomplete': 'off',
                'type': 'password',
            }
        ),
    )
    org_name = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('укажите название компании')},
        widget=TextInput(
            attrs={
                'placeholder': 'Название компании',
                'autocomplete': 'off',
            }
        ),
    )

    def clean_phone_number(self):
        _phone_number = self.cleaned_data.get('phone_number')

        if User.objects.filter(phone_number=_phone_number).exists():
            raise ValidationError(_('пользователь с таким номером уже существует'))
        return _phone_number

    def clean_password2(self):
        _password = self.cleaned_data.get('password')
        _password2 = self.cleaned_data.get('password2')

        if _password != _password2:
            raise ValidationError(_('пароли не совподают'))

        return _password2


class ChangePasswordForm(Form):
    password = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('укажите пароль')},
        widget=TextInput(
            attrs={
                'placeholder': 'Введите новый пароль',
                'autocomplete': 'off',
                'type': 'password',
            }
        ),
    )
    password2 = CharField(
        max_length=255,
        required=True,
        error_messages={'required': _('повторите пароль')},
        widget=TextInput(
            attrs={
                'placeholder': 'Подтвердите новый пароль',
                'autocomplete': 'off',
                'type': 'password',
            }
        ),
    )
    phone_number = CharField(
        max_length=20,
        widget=TextInput(
            attrs={'id': 'phone_phone_id'}
        )
    )

    def clean_password2(self):
        _password = self.cleaned_data.get('password')
        _password2 = self.cleaned_data.get('password2')

        if _password != _password2:
            raise ValidationError(_('пароли не совподают'))

        return _password2
