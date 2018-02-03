"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import yaml
import logging
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from corsheaders.defaults import default_headers
from django.core.exceptions import ImproperlyConfigured

def os.environ.get(var_name):
    """ Get environment variable or raise the exception """

    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(PROJECT_ROOT, 'app')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(1, PROJECT_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nje62b1kyvvc1!g_d@5a5qq!2bs6jl)isr^91cm=gv1&_h6m^5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers
ES_CLIENT = Elasticsearch(['http://elasticsearch:9200'])
connections.create_connection(hosts=['elasticsearch'])
docker_env = os.environ.get('DOCKER_ENV')

if os.path.isfile('app/secrets.yaml'):
    with open('app/secrets.yaml') as stream:
        f = yaml.load(stream)
        for k, v in f.items():
            os.environ[k] = v

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'anymail',
    'corsheaders',
    'django_nose',
    'easy_thumbnails',
    'authorization',
    'profiles',
    'companies',
    'skills',
    'vacancies',
    'interviews',
    'feedbacks',
    'notifications',
    'attachments',
    'resumes',
    'storages'
]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'app.urls'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

if 'test' in sys.argv:
    logging.disable(logging.CRITICAL)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'app/templates'
        ],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

docker_db = {
    'HOST': 'db',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'PORT': 5432
}
vagrant_db = {
    'HOST': 'localhost',
    'USER': 'vagrant',
    'PASSWORD': 'vagrant',
    'PORT': 5432
}

if docker_env:
    db_config = docker_db
else:
    db_config = vagrant_db

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'interview_manager',
        'USER': db_config['USER'],
        'PASSWORD': db_config['PASSWORD'],
        'HOST': db_config['HOST'],
        'PORT': db_config['PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SERVER_NAME')
}
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')  # or sendgrid.EmailBackend, or...
DEFAULT_FROM_EMAIL = "you@example.com"  # if you don't already have this in settings

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'authorization.User'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-spec', '--spec-color']
FIXTURE_DIRS = (os.path.join(BASE_DIR, 'app', 'fixtures'),)
if docker_env:
    username = os.environ.get('RABBITMQ_DEFAULT_USER')
    password = os.environ.get('RABBITMQ_DEFAULT_PASS')
    broker = 'amqp://{}:{}@rabbit'.format(username, password)
else:
    broker = 'amqp://localhost'
CELERY_BROKER_URL = broker
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_ACCESS_KEY_ID = os.environ.get('S3_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
THUMBNAIL_BASEDIR = 'thumbs'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'app.storage_backends.MediaStorage'

THUMBNAIL_ALIASES = {
    '': {
        'small_thumb': {'size': (50, 50) },
        'thumb': {'size': (100, 100) },
        'medium': {'size': (200, 200) },
        'medium_large': {'size': (250, 250) },
        'large': {'size': (350, 350) }
    },
}
THUMBNAIL_FORCE_OVERWRITE = True
