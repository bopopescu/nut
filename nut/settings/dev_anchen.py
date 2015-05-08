from stage import *


TEMPLATE_CONTEXT_PROCESSORS += (
    # 'apps.web.contextprocessors.global.lastslug',
)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'guoku',
        'PASSWORD': 'guoku!@#',
        'HOST': '10.0.2.90',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}


__author__ = 'an chen '
