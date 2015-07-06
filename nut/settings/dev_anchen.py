from stage import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

IMAGE_HOST = 'http://images.hello.new/'


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

TEMPLATE_STRING_IF_INVALID = "****************** %s ****************"


__author__ = 'an chen '
