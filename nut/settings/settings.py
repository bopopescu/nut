# coding=utf-8
"""
Django settings for nut project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import environ
from secret_settings import *
from celery.schedules import crontab

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 1

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = django_secret_key
DEBUG = False
TESTING = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
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
    'captcha',
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

HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_CUSTOM_HIGHLIGHTER = 'apps.web.highlighter.MyHighlighter'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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

CACHES = {
    'default': env.cache('REDIS_CACHE_URL')
}


TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

SITE_DOMAIN = 'www.guoku.com'

LOCALE_PATHS = (
    os.path.join(os.getcwd(), 'conf/locale'),
)

STATICFILES_DIRS = (
    os.path.join(os.getcwd(), 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'apps.web.contextprocessors.global.last_slug',
    'apps.web.contextprocessors.global.browser',
    'apps.web.contextprocessors.global.check_is_from_mobile',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'size',
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

EMAIL_BACKEND = 'sendcloud.SendCloudBackend'
MAIL_APP_USER = 'guoku_hi'
MAIL_APP_KEY = 'DLq9W6TiDZAWOLNv'
MAIL_LIST = 'all_gkusers@maillist.sendcloud.org'
GUOKU_MAIL = 'hi@mail.guoku.com'
GUOKU_NAME = u'果库'
MAIL_EDM_USER = 'guoku_edm3'

RESET_PASSWORD_TEMPLATE = 'forget_password'
VERFICATION_EMAIL_TEMPLATE = 'verify_email'


STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'

AUTH_USER_MODEL = 'core.GKUser'

IMAGE_HOST = 'http://imgcdn.guoku.com/'

# img counter for article feeds
IMG_COUNTER_HOST = 'http://www.guoku.com'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

Avatar_Image_Path = 'avatar/'

# Fetch articles.
CELERY_DISABLE_RATE_LIMITS = False
CELERY_ROUTES = {
    'sogou.crawl_articles': {'queue': 'sogou'},
    'sogou.fetch_article_list': {'queue': 'sogou'},
}

CELERY_ANNOTATIONS = {
    'sogou.crawl_articles': {
        'rate_limit': '1/m',
    },
    'sogou.fetch_article_list': {
        'rate_limit': '1/m',
    },
}

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
# CAPTCHA_CHALLENGE_FUNCT = 'apps.core.utils.captcha.chinese_math_challenge'

# for debug server popular  category test
DEFAULT_POPULAR_SCALE = 7

INTERVAL_OF_SELECTION = 24

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

CLICK_HOST = 'http://click.guoku.com'

# Sentry
RAVEN_CONFIG = {
    'dsn': 'https://562f3c643ffb4a3384a0bacbce38c87c:be8c376f3a29447ea4318f454f8a650a@sentry.frozenpear.net/3',
}

CHECK_BUY_LINK_URL = env.str('CHECK_BUY_LINK_URL')

OSS_REGION = env.str('OSS_REGION')
OSS_ACCESS_KEY_ID = env.str('OSS_ACCESS_KEY_ID')
OSS_ACCESS_KEY_SECRET = env.str('OSS_ACCESS_KEY_SECRET')
OSS_BUCKET = env.str('OSS_BUCKET')
OSS_ENDPOINT = env.str('OSS_ENDPOINT')

MOGILEFS_MEDIA_URL = 'images/'

FIXTURE_DIRS = []