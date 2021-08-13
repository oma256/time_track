import environ

env = environ.Env()

DEBUG = env.str('DJANGO_DEBUG', default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'worktime_db',
        'USER': 'worktime_db_user',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}