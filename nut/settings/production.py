# coding=utf-8
import environ
from settings import *

env = environ.Env()

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_URL = 'https://scdn.guoku.com/static/v4/3cdb8ef6099192963dee1318e9ba46e89d1cea20/'

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

DATABASES = {
    'default': env.db(),
    'slave': env.db(),
}

INSTALLED_APPS += (
    'gunicorn',
)

DEFAULT_CHARSET = "UTF-8"

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_FILE_PATH = '/tmp/django'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

MOGILEFS_MEDIA_URL = 'images/'
# DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'
DEFAULT_FILE_STORAGE = 'utils.django_oss_storage.OSSStorage'


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
    'default': env.search_url()
}

SINA_APP_KEY = '1459383851'
SINA_APP_SECRET = 'bfb2e43c3fa636f102b304c485fa2110'
SINA_BACK_URL = 'http://www.guoku.com/sina/auth'

SITE_HOST = 'http://www.guoku.com'

django_secret_key = 'zl4j09adh-*tv7-b5&(zu!nkudhry*yy1b9--$%)&yh^4caq_7'

CELERY_RESULT_BACKEND = "redis://:Pt2fkfAvPhqNPFwECBUZ36yagGfFGd2a3J9wLFGHjcfZCk4XuyWsdRKo2qr7jj9t@47.92.91.9:10086/1"
CELERY_IGNORE_RESULT = False
CELERY_TIMEZONE = 'Asia/Shanghai'

BROKER_URL = 'redis://:Pt2fkfAvPhqNPFwECBUZ36yagGfFGd2a3J9wLFGHjcfZCk4XuyWsdRKo2qr7jj9t@47.92.91.9:10086/2'

CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1

# taobao
APP_HOST = "http://www.guoku.com"
TAOBAO_APP_KEY = '12313170'
TAOBAO_APP_SECRET = '90797bd8d5859aac971f8cc9d4e51105'
# TAOBAO_APP_KEY = '23145551'
# TAOBAO_APP_SECRET = 'a6e96561f12f62515f7ed003b1652b94'
TAOBAO_OAUTH_URL = 'https://oauth.taobao.com/authorize'
TAOBAO_OAUTH_LOGOFF = 'https://oauth.taobao.com/logoff'
TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"
TAOBAO_APP_INFO = {
    "default_app_key": "12313170",
    "default_app_secret": "90797bd8d5859aac971f8cc9d4e51105",
    "web_app_key": "21419640",
    "web_app_secret": "df91464ae934bacca326450f8ade67f7"
}

BAICHUAN_APP_KEY = '23093827'
BAICHUAN_APP_SECRET = '5a9a26e067f33eea258510e3040caf17'

# wechatfi
WECHAT_TOKEN = 'guokuinwechat'
WECHAT_APP_ID = 'wx728e94cbff8094df'
WECHAT_APP_SECRET = 'd841a90cf90d00f145ca22b82e12a500'

# jpush
JPUSH_KEY = 'f9e153a53791659b9541eb37'
JPUSH_SECRET = 'a0529d3efa544d1da51405b7'

ALIPAY_MD5_KEY = 'sij86zv335q7fb2k54iznoxg6s2z19g2'
ALIPAY_PID = '2088511535586742'
