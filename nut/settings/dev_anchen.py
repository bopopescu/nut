import sys
from stage import *
DEBUG = True

TESTING = len(sys.argv) > 0 and sys.argv[0].endswith('py.test')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# for article related celery task
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
#
IMAGE_HOST = 'http://imgcdn.guoku.com/'
#

# LOCAL_IMG_DEBUG=True
# IMAGE_HOST = 'http://127.0.0.1:9766/'
# INTRANET_IMAGE_SERVER = 'http://images.hello.new/'
# MEDIA_ROOT='/media/upload/'
# AVATAR_HOST = IMAGE_HOST


IMG_COUNTER_HOST = 'http://127.0.0.1:9766'


#for mobile access simulation
ANT_SIMULATE_MOBILE = True

#for local solr search

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://10.0.2.115:8983/solr/',
#         'INCLUDE_SPELLING': True,
#         # 'PATH': os.path.join(os.path.dirname(__file__), '../whoosh_index'),
#     }
# }
# # HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_DEFAULT_OPERATOR = 'OR'


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

INSTALLED_APPS +=(
        'django.contrib.sessions',
        'django.contrib.admin'
)

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
