"""
local settings, will overwrite dian/settings
"""


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

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'dian'


# md5 seed

MD5_SEED = 'dk26.com'


# django-cors-headers settings, 

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:9000',
    'localhost:9000',
)


# qiniu settings

QINIU_ACCESS_KEY = "WbBF2OGhoW23qBTcNkdgmpuvDgI3S-m-IzIz0xTp"
QINIU_SECRET_KEY = "zykcP-49eXiX53kQR3nsLQHDXbg9FW5avL4OSOvD"
QINIU_BUCKET_PUBLIC = "dian"
