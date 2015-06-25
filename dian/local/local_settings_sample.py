"""
local settings, will overwrite dian/settings
"""
DEBUG = False

# ref: https://docs.djangoproject.com/en/1.7/ref/settings/
ALLOWED_HOSTS = (
    'diankuai.cn',
    '127.0.0.1:9000',
    'localhost:9000',
    '127.0.0.1:3000',
    'localhost:3000',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'dian',                      # Or path to database file if using sqlite3.
#         'USER': 'dian',                      # Not used with sqlite3.
#         'PASSWORD': '123456',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Mongo settings

# MONGO_HOST = '127.0.0.1'
# MONGO_PORT = 27017
# MONGO_DB = 'dian'


# md5 seed

MD5_SEED = 'diankuai.cn'


# django-cors-headers settings, 

CORS_ORIGIN_WHITELIST = (
    'diankuai.cn',
    'www.diankuai.cn',
    'api.diankuai.cn',
    'c.diankuai.cn',
    'wp.diankuai.cn',
    '127.0.0.1:9000',
    'localhost:9000',
    '127.0.0.1:3000',
    'localhost:3000',
)


# qiniu settings

QINIU_ACCESS_KEY = "WbBF2OGhoW23qBTcNkdgmpuvDgI3S-m-IzIz0xTp"
QINIU_SECRET_KEY = "zykcP-49eXiX53kQR3nsLQHDXbg9FW5avL4OSOvD"
QINIU_BUCKET_PUBLIC = "dian"
QINIU_DOMAIN = "http://7u2ghq.com1.z0.glb.clouddn.com/"


# Weixin configration

APP_ID = 'wx8f2xfe405cfec552c'
APP_SECRET = '8c114x06f05e2e242ca5638b883482a31'


# API domain

API_DOMAIN = "http://api.diankuai.cn/"


# Weixin platform

WP_DOMAIN = "http://wp.diankuai.cn/"

