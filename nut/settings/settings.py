"""
Django settings for nut project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# import sys
# sys.setrecursionlimit(10000) # 10000 is an example, try with different values

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zl4j09adh-*tv7-b5&(zu!nkudhry*yy1b9--$%)&yh^4caq_7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'rest_framework',
    # 'rest_framework.authtoken',
    # 'haystack',
    'djcelery',
    # 'notifications',

    'apps.core',
    'apps.management',
    'apps.web',
    'apps.mobile',
    'apps.images',
    'apps.wechat',
    'apps.notifications',
    'apps.report',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://10.0.2.46:6379/1",
            "redis://10.0.2.47:6379/1",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            "PICKLE_VERSION": -1,
            "SOCKET_TIMEOUT": 5,  # in seconds
            "COMPRESS_MIN_LEN": 10,
            "CONNECTION_POOL_KWARGS": {"max_connections": 1024}
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '../conf/locale'),
)

STATICFILES_DIRS = (
    os.path.join(os.getcwd(), 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',
    # 'django.core.context_processors.debug',
    'django.core.context_processors.static',
)


# rest framework
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.AllowAny',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.'
    # ],
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'size',
}

# mail
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-7n8gut3y8rpk1u-0edgmgaj7vs50gig8'
MAILGUN_SERVER_NAME = 'post.guoku.com'
EMAIL_SUBJECT_PREFIX = '[guoku]'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'

AUTH_USER_MODEL = 'core.GKUser'

IMAGE_HOST = 'http://imgcdn.guoku.com/'


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# IMAGE_SIZE = [128, 310, 640]

Avatar_Image_Path = 'avatar/'
# Avatar_Image_Size = [180, 50]


HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'apps.core.backends.whoosh_guoku_backend.GkEngine',
        'PATH': os.path.join(os.path.dirname(__file__), '../whoosh_index'),
    }
}
HAYSTACK_DEFAULT_OPERATOR = 'OR'


# WHOOSH_INDEX = 'indexdir'



# celery
# from __future__ import absolute_import

# BROKER_URL = 'redis://10.0.2.95:6379/10'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = "redis://10.0.2.95:6379/0"
BROKER_TRANSPORT = "librabbitmq"
BROKER_HOST = "10.0.2.95"
BROKER_USER = "raspberry"
BROKER_PASSWORD = "raspberry1@#"
BROKER_VHOST = "raspberry"
BROKER_POOL_LIMIT = 10
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_DISABLE_RATE_LIMITS = True
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'



SPHINX_API_VERSION = 0x116
SPHINX_SERVER = '10.0.2.50'
SPHINX_PORT = 3312


# taobao
APP_HOST = "http://www.guoku.com"
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
# TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"

# wechat
WeChatToken = 'guokuinwechat'