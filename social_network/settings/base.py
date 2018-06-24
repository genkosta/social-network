"""
Django settings.
"""

import os
from .pipeline_conf import PIPELINE

PROJECT_NAME = 'social_network'
PASSWORD_DB_DEV = 'WA7uUG5qrNs5J7V9'
PASSWORD_DB_PROD = 'XMh7brCHuWMw32Wa'

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
root_path = lambda *args: os.path.join(ROOT, *args)
path = lambda *args: os.path.join(BASE_DIR, *args)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7(-31+(o5z^9hxih7!754lk*w1t_t#po#pibcn*89hp^ud)%8-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = [('admin', 'genkosta43@gmail.com')]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # add-ons
    'pipeline',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    # apps
    PROJECT_NAME,
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_NAME)

# Internationalization
LANGUAGE_CODE = 'ru'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

MEDIA_ROOT = root_path('media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = '/tmp/{}/static'.format(PROJECT_NAME)

# Additional locations of static files
STATICFILES_DIRS = (
    path('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',  # For django-pipeline
)

# For django-pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@site.net'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DATA_UPLOAD_MAX_MEMORY_SIZE = 4194304

# Web API
CORS_ORIGIN_ALLOW_ALL = True
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope'
    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
