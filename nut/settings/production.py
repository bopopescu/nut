from secret_settings import *
from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_URL = 'https://scdn.guoku.com/static/v4/3cdb8ef6099192963dee1318e9ba46e89d1cea20/'

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

DATABASES = PRODUCTION_DATABASES

INSTALLED_APPS += (
    'gunicorn',
)

DEFAULT_CHARSET = "UTF-8"

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_FILE_PATH = '/tmp/django'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'

Avatar_Image_Path = 'avatar/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/django.log',
            'mode': 'a',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'sentry'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://10.0.2.115:8983/solr/',
        'INCLUDE_SPELLING': True,
    }
}

SINA_APP_KEY = '1459383851'
SINA_APP_SECRET = 'bfb2e43c3fa636f102b304c485fa2110'
SINA_BACK_URL = APP_HOST + '/sina/auth'

# config of site in redis.
CONFIG_REDIS_HOST = '10.0.2.95'
CONFIG_REDIS_PORT = 6379
CONFIG_REDIS_DB = 10

SITE_HOST = 'http://www.guoku.com'
