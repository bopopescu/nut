from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# STATIC_URL = 'http://static.guoku.com/static/v4/d6d8bc3600a44816fbf1ebcfacd2de45c32cc359/'

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        'PASSWORD': 'guoku1@#',
        'HOST': '10.0.2.125',
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        'PASSWORD': 'guoku1@#',
        'HOST': '10.0.2.125',
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

# CELERY #################################
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYD_CONCURRENCY = 2
CELERY_DISABLE_RATE_LIMITS = False
#celery end  #############################
import djcelery
djcelery.setup_loader()

# config of site in redis.
CONFIG_REDIS_HOST = 'localhost'
CONFIG_REDIS_PORT = 6379

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '//libs.baidu.com/jquery/2.1.4//jquery.min.js'
}


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
)

MIDDLEWARE_CLASSES += (
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
)

INSTALLED_APPS += (
    'gunicorn',
    'debug_toolbar',
    # 'haystack'
)

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://10.0.2.48:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp/'

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"

MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
<<<<<<< HEAD
LOCAL_IMG_DEBUG = True
IMAGE_HOST = 'http://imgcdn.guoku.com/'
INTRANET_IMAGE_SERVER = 'http://localhost:5556/'
=======
# IMAGE_SIZE = [128, 310, 640]
>>>>>>> 18ff1484fa612410848f0118ff3712b419d2be72

Avatar_Image_Path = 'avatar/'
# Avatar_Image_Size = [180, 50]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
          'level': 'INFO',
          'class': 'logging.FileHandler',
          'formatter': 'verbose',
          'filename': '/tmp/django.log',
          'mode': 'a',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file',],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


# IMAGE_HOST = 'http://image.guoku.com/'


APP_HOST = "http://test.guoku.com"
TAOBAO_APP_KEY = '12313170'
TAOBAO_APP_SECRET = '90797bd8d5859aac971f8cc9d4e51105'
TAOBAO_OAUTH_URL = 'https://oauth.taobao.com/authorize'
TAOBAO_OAUTH_LOGOFF = 'https://oauth.taobao.com/logoff'
TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"
TAOBAO_APP_INFO = {
    "default_app_key" : "12313170",
    "default_app_secret" : "90797bd8d5859aac971f8cc9d4e51105",
    "web_app_key" : "21419640",
    "web_app_secret" : "df91464ae934bacca326450f8ade67f7"
}


# weibo
SINA_APP_KEY = '2830558576'
SINA_APP_SECRET = 'a4861c4ea9facd833eb5d828794a2fb2'
SINA_BACK_URL = APP_HOST + '/sina/auth'

# wechat
WECHAT_TOKEN = 'guokuinwechat'
WECHAT_APP_ID = 'wx865ef8a1231580c5'
WECHAT_APP_SECRET = '98c99129bb86afc010810b66d62a0b1c'

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://10.0.2.115:8983/solr/',
        'INCLUDE_SPELLING': True,
        # 'PATH': os.path.join(os.path.dirname(__file__), '../whoosh_index'),
    }
}
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_DEFAULT_OPERATOR = 'OR'

__author__ = 'edison7500'
