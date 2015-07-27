from stage import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        # 'LOCATION': '/tmp/django_cache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guoku',
        'USER': 'root',
        'PASSWORD': 'happystudy',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

__author__ = 'huiter'
