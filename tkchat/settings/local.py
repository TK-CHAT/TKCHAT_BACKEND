from .base import *

import environ
# Initialise environment variables 
env = environ.Env()
environ.Env.read_env()


ALLOWED_HOSTS = ['*']
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('NAME_DB'),
        'USER': env('USER_DB'),
        'PASSWORD': env('PASSWORD_DB'),
        'HOST': env('HOST_DB'),
        'PORT': env('PORT_DB')
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
