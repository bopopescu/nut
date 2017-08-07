# coding=utf-8
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

from secret_settings import *
from celery.schedules import crontab


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  django_secret_key
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TESTING = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
# Application definition

'''
    https header forwarded
'''
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'haystack',
    'djcelery',
    # 'notifications',

    'captcha', #验证码

    'apps.core',
    'apps.management',
    'apps.web',
    'apps.mobile',
    'apps.images',
    'apps.wechat',
    'apps.notifications',
    'apps.report',
    'apps.counter',
    'apps.tag',
    'apps.seller',
    'apps.shop',
    'apps.site_banner',
    'apps.order',
    'apps.payment',
    'apps.top_ad',
    'apps.offline_shop',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://10.0.2.110:8983/solr/',
        'INCLUDE_SPELLING': True,
        # 'PATH': os.path.join(os.path.dirname(__file__), '../whoosh_index'),
    }
}
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_CUSTOM_HIGHLIGHTER = 'apps.web.highlighter.MyHighlighter'

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
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

PRODUCTION_REDIS_SERVER = True
PRODUCTION_REDIS_SERVER_HOST = '10.0.2.46'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://10.0.2.46:6379/1",
            "redis://10.0.2.120:6379/1",
            "redis://10.0.2.115:6379/1",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            "PICKLE_VERSION": -1,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,  # in seconds
            "COMPRESS_MIN_LEN": 10,
            "CONNECTION_POOL_KWARGS": {"max_connections": 1024},
            "PARSER_CLASS": "redis.connection.HiredisParser",
        }
    },

}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

SITE_DOMAIN = 'www.guoku.com'
# USE_TZ = True

LOCALE_PATHS = (
    # os.path.join(os.path.dirname(__file__), '../conf/locale'),
    os.path.join(os.getcwd(), 'conf/locale'),
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
    #add by an , for event slug insert into every page.
    # see document for reason,
    # modified base.html (template) for this processor to take effect
    'apps.web.contextprocessors.global.last_slug',
    'apps.web.contextprocessors.global.browser',
    'apps.web.contextprocessors.global.check_is_from_mobile',
)


# rest framework
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAdminUser',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authtoken',
    # ],
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'size',
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# mail

# EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
# MAILGUN_ACCESS_KEY = 'key-7n8gut3y8rpk1u-0edgmgaj7vs50gig8'
EMAIL_BACKEND = 'sendcloud.SendCloudBackend'
MAIL_APP_USER = 'guoku_hi'
MAIL_APP_KEY = 'DLq9W6TiDZAWOLNv'
# MAIL_LIST = 'test_edm@maillist.sendcloud.org'
MAIL_LIST = 'all_gkusers@maillist.sendcloud.org'
GUOKU_MAIL = 'hi@mail.guoku.com'
GUOKU_NAME = u'果库'
MAIL_EDM_USER = 'guoku_edm3'

RESET_PASSWORD_TEMPLATE = 'forget_password'
VERFICATION_EMAIL_TEMPLATE = 'verify_email'



# MAILGUN_SERVER_NAME = 'post.guoku.com'
# EMAIL_SUBJECT_PREFIX = '[guoku]'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'

AUTH_USER_MODEL = 'core.GKUser'

IMAGE_HOST = 'http://imgcdn.guoku.com/'

#img counter for article feeds
IMG_COUNTER_HOST = 'http://www.guoku.com'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# IMAGE_SIZE = [128, 310, 640]

Avatar_Image_Path = 'avatar/'
# Avatar_Image_Size = [180, 50]

# WHOOSH_INDEX = 'indexdir'

# celery
# from __future__ import absolute_import

# BROKER_URL = 'redis://10.0.2.95:6379/10'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'


# Fetch articles.
CELERY_DISABLE_RATE_LIMITS = False
CELERY_ROUTES = {
    'sogou.crawl_articles': {'queue': 'sogou'},
    # 'sogou.crawl_article': {'queue': 'sogou'},
    'sogou.fetch_article_list': {'queue': 'sogou'},
}

CELERY_ANNOTATIONS = {
    'sogou.crawl_articles': {
        'rate_limit': '1/m',
    },
    # 'sogou.crawl_article': {
    #     'rate_limit': '1/m',
    # },
    'sogou.fetch_article_list': {
        'rate_limit': '1/m',
    },
}
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERY_ROUTES = {
    'sogou.crawl_articles': {'queue': 'sogou'},
    'sogou.crawl_article': {'queue': 'sogou'},
    'sogou.fetch_article_list': {'queue': 'sogou'},
}



# for django-simple-captcha
CAPTCHA_FOREGROUND_COLOR = '#ffffff'
CAPTCHA_BACKGROUND_COLOR = '#000000'
CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_arcs',
    # 'captcha.helpers.noise_dots',
)
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_LENGTH = 8
# CAPTCHA_FONT_PATH = 'fonts/planetbe.ttf'
CAPTCHA_FONT_PATH = 'fonts/kai.ttf'
CAPTCHA_FONT_SIZE = 30
CAPTCHA_CHALLENGE_FUNCT = 'apps.core.utils.captcha.chinese_math_challenge'

# for debug server popular  category test
DEFAULT_POPULAR_SCALE = 7

# config of site in redis.
CONFIG_REDIS_HOST = 'localhost'
CONFIG_REDIS_PORT = 6379
CONFIG_REDIS_DB = 1

INTERVAL_OF_SELECTION = 24

# phantom
PHANTOM_SERVER = 'http://10.0.2.49:5000/'

# fetch articles
SOGOU_PASSWORD = 'guoku1@#'
SOGOU_USERS = ('shoemah55@superrito.com',
               'monan1977@fleckens.hu',
               'obsomed1977@jourrapide.com',
               'finighboy78@superrito.com',
               'artimessill1959@einrot.com',
               'suildrued41@dayrep.com',
               'ater1954@teleworm.us',
               'duad1937@jourrapide.com',
               'drecur44@superrito.com',
               'paboy1973@superrito.com'
               )

CELERYBEAT_SCHEDULE = {
    'crawl_articles': {
        'task': 'sogou.crawl_articles',
        'schedule': crontab(minute=1, hour=1)
    }
}

FETCH_INTERVAL = 20
CURRENCY_SYMBOLS = (u'$', u'￥')


TAOBAO_RECOMMEND_URL = 'http://10.0.2.120:10150/recommend'
ARTICLE_TEXTRANK_URL = 'http://10.0.2.120:10150/article/'

CLICK_HOST = 'http://click.guoku.com'

# Sentry
RAVEN_CONFIG = {
    'dsn': 'http://93c33ee5ff4c4db1b8fc65d4a971e641:de869c769f8d405696285368d489bdfc@sentry.guoku.com/2',
}
