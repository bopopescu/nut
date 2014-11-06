from settings import *

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'qinzhoukan',
        'PASSWORD': 'qinzhoukan1@#',
        'HOST': '10.0.2.90',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}


INSTALLED_APPS += (
    'gunicorn',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp/django'

MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
IMAGE_SIZE = [128, 310, 640]

Avatar_Image_Path = 'avatar/'
Avatar_Image_Size = [180, 50]


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
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

__author__ = 'edison7500'
