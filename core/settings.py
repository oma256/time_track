import os

import environ


env = environ.Env()
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='not_a_secret')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'rest_framework',
    'rest_framework.authtoken',

    'apps.users',
    'apps.organizations',
    'apps.api',
    'apps.payment',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates', 'assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = 'users:login'

# PAYBOX SECTION
PAYBOX_PROJECT_ID = env.str('PAYBOX_PROJECT_ID', default='123456')
PAYBOX_SECRET_KEY = env.str('PAYBOX_SECRET_KEY', default='123456')
PAYBOX_SALT = env.str('PAYBOX_SALT', default='123456')
PAYBOX_SUCCESS_URL_METHOD = env.str('PAYBOX_SUCCESS_URL_METHOD', default='GET')
PAYBOX_CURRENCY = env.str('PAYBOX_CURRENCY', default='KGS')
PAYBOX_LANGUAGE = env.str('PAYBOX_LANGUAGE', default='ru')
PAYBOX_URL = env.str(
    'PAYBOX_URL', default='https://api.paybox.money/payment.php',
)
PAYBOX_SUCCESS_URL = env.str(
    'PAYBOX_SUCCESS_URL', default='http://a380c1b46bcb.ngrok.io',
)
PAYBOX_RESULT_URL = env.str(
    'PAYBOX_RESULT_URL',
    default='http://a380c1b46bcb.ngrok.io/payment/paybox-result/',
)

SITE_PROTOCOL = env.str('SITE_PROTOCOL', default='http')
SITE_DOMAIN = env.str('SITE_DOMAIN', default='localhost')

try:
    from core.conf.local import *
except ImportError:
    from core.conf.production import *
