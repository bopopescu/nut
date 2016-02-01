from stage import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        # 'PASSWORD': 'guoku!@#',
        # 'HOST': '10.0.2.90',
        'PASSWORD': 'guoku1@#',
        'HOST': '10.0.2.125',
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },

    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        # 'PASSWORD': 'guoku!@#',
        # 'HOST': '10.0.2.95',
        'PASSWORD': 'guoku1@#',
        'HOST': '10.0.2.125',
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

# CELERY #################################
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYD_CONCURRENCY = 2
CELERY_DISABLE_RATE_LIMITS = False
CELERY_IMPORTS = ('apps.fetch.article.weixin',)
#celery end  #############################
import djcelery
djcelery.setup_loader()
