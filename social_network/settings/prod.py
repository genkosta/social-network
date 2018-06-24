# -*- coding: utf-8 -*-
from .base import *


NAME_DB = '{}_prod'.format(PROJECT_NAME)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': NAME_DB,
        'USER': NAME_DB,
        'PASSWORD': PASSWORD_DB_PROD,
        'HOST': '',
        'PORT': '',
    }
}

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

STATIC_ROOT = os.path.abspath(root_path('..', '..', 'static'))
MEDIA_ROOT = os.path.abspath(root_path('..', '..', 'media'))
STATUS_PROJECT = 'prod'
