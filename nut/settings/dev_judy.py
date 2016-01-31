import sys
from stage import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEBUG = True
TESTING = len(sys.argv) > 0 and sys.argv[0].endswith('py.test')
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# http://docs.celeryproject.org/en/2.5/getting-started/brokers/redis.html#broker-redis
# CELERY #################################
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#celery end  #############################
import djcelery
djcelery.setup_loader()

# phantom
PHANTOM_SERVER = 'http://192.168.99.100:5000/'

# config of site in redis.
CONFIG_REDIS_HOST = 'localhost'
CONFIG_REDIS_PORT = 6379

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
    }
}


def removeDebugToolBar(theList):
    return [x for x in theList if x != 'debug_toolbar']

INSTALLED_APPS = removeDebugToolBar(INSTALLED_APPS)

LOCAL_TEST_DB = True

Current_Dbhost = 'localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': Current_Dbhost,
        'PORT': '3306',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
            }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': Current_Dbhost,
        'PORT': '3306',
        'OPTIONS': {
            'use_unicode': 'utf-8',
            'init_command': 'SET storage_engine=INNODB'
            },
        # 'TEST_MIRROR': 'default'
    },
    }

# need this for popular category like back trace time
#  the test server will have very little entity like data
# so the default popular backtrace day count will be 200
# in production , the number will be 7  , in settings.py file
DEFAULT_POPULAR_SCALE = 200


RESET_PASSWORD_TEMPLATE = 'forget_password'
VERFICATION_EMAIL_TEMPLATE = 'verify_email'
INTERVAL_OF_SELECTION = 24


IMAGE_HOST = 'http://127.0.0.1:8000/'
MOGILEFS_MEDIA_URL = 'images/'
LOCAL_IMG_DEBUG = True
INTRANET_IMAGE_SERVER = 'http://127.0.0.1:8001/'

# mail
MAIL_LIST_ADDR='test_edm'
MAIL_LIST = 'test_edm@maillist.sendcloud.org'
