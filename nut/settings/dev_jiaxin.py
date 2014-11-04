from production import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
)

__author__ = 'edison7500'
