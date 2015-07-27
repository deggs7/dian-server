"""
Django settings for dian project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i4lzccdofu6#mbkc8@wwok-0q)i6ysdkz6^q6wp5$+=c7@2lp&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'djcelery',
    'corsheaders',
    'rest_framework',
    'dian',
    'account',
    'restaurant',
    'registration',
    'table',
    'menu',
    'photo',
    'trade',
    'wechat',
    'reward',
    'game',
    'rest_framework.authtoken',
    'south',
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restaurant.middleware.RestaurantMiddleware',
    'account.middleware.MemberMiddleware',
)

ROOT_URLCONF = 'dian.urls'

WSGI_APPLICATION = 'dian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Template
TEMPLATE_LOADERS = (
    # 'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# Custom User

AUTH_USER_MODEL = 'account.User'


# Django REST Framework Settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


# django-cors-headers settings,
# https://github.com/ottoyiu/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:9000',
    'localhost:9000',
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'Content-Type',
    'Authorization',
    'X-Restaurant-Id',
    'X-Member-Id',
)


# celery
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://dian:dian@localhost:5672/dianvhost'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# msg
MSG_ACCOUNT = "13021045329"
MSG_PASSWORD = "28788DE1EDAF72E75A1BFAF2F98E"


# md5 seed

MD5_SEED = 'diankuai.cn'


# qiniu settings

QINIU_ACCESS_KEY = "WbBF2OGhoW23qBTcNkdgmpuvDgI3S-m-IzIz0xTp"
QINIU_SECRET_KEY = "zykcP-49eXiX53kQR3nsLQHDXbg9FW5avL4OSOvD"
QINIU_BUCKET_PUBLIC = "dian"
QINIU_DOMAIN = "http://7u2ghq.com1.z0.glb.clouddn.com/"


# Weixin configration

APP_ID = 'wx8f2xfe405cfec552c'
APP_SECRET = '8c114x06f05e2e242ca5638b883482a31'


# Temporary directory

TEMP_DIR = "/tmp/temp_diankuai/"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# API domain

API_DOMAIN = "http://api.diankuai.cn/"


# Weixin platform

WP_DOMAIN = "http://wp.diankuai.cn/"


# Overwrite configuration

try:
    from local.local_settings import *
except Exception, e:
    print e


# http://www.django-rest-framework.org/api-guide/authentication

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d\
            %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'dian-server-log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'dian': {
            'handlers': ['console', 'file'] if DEBUG else ['file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            # 'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'level': 'DEBUG',
        },
    },
}


