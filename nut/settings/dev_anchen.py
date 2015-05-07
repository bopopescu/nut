from stage import *


TEMPLATE_CONTEXT_PROCESSORS += (
    # 'apps.web.contextprocessors.global.lastslug',
)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guoku',
        'USER': 'root',
        'PASSWORD': 'mypass740323',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}



__author__ = 'an chen '
