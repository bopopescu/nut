from stage import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

IMAGE_HOST = 'http://imgcdn.guoku.com/'
AVATAR_HOST = 'http://imgcdn.guoku.com/'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# http://docs.celeryproject.org/en/2.5/getting-started/brokers/redis.html#broker-redis
# CELERY #################################
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#celery end  #############################
import djcelery
djcelery.setup_loader()


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }
#

# ----------------------- debug -----------------------
def removeDebugToolBar(theList):
    return [x  for x in theList if x!='debug_toolbar']

INSTALLED_APPS = removeDebugToolBar(INSTALLED_APPS)

#-------------------------debug end --------------------


# TEMPLATE_CONTEXT_PROCESSORS += (
#     # 'apps.web.contextprocessors.global.lastslug',
# )
LOCAL_TEST_DB = True

Current_Dbhost = 'localhost'
# Current_Dbhost = '10.0.1.110'
# Current_Dbhost = '10.0.2.90'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        'PASSWORD': 'guoku!@#',
        'HOST': Current_Dbhost,
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        'PASSWORD': 'guoku!@#',
        'HOST': Current_Dbhost,
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

# need this for popular category like back trace time
#  the test server will have very little entity like data
# so the default popular backtrace day count will be 200
# in production , the number will be 7  , in settings.py file
DEFAULT_POPULAR_SCALE = 200

# class InvalidString(str):
#     def __mod__(self, other):
#         from django.template.base import TemplateSyntaxError
#         raise TemplateSyntaxError(
#             "Undefined variable or unknown value for: \"%s\"" % other)
#
# TEMPLATE_STRING_IF_INVALID = "****************** %s ****************"


__author__ = 'an chen '
