from production import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
)

__author__ = 'edison7500'
