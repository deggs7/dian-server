"""
local settings, will overwrite bangx2/settings
"""


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'bangx2',                      # Or path to database file if using sqlite3.
#         'USER': 'bangx2',                      # Not used with sqlite3.
#         'PASSWORD': '123456',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Mongo settings

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'bangx2'


# md5 seed

MD5_SEED = 'bangx2.com'


# django-cors-headers settings, 

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:9000',
)


# qiniu settings

import qiniu.conf
qiniu.conf.ACCESS_KEY = "<YOUR_APP_ACCESS_KEY>"
qiniu.conf.SECRET_KEY = "<YOUR_APP_SECRET_KEY>"

QINIU_UPLOAD_PUBLIC = "bang"
QINIU_UPLOAD_PRIVATE = "bang-security"
