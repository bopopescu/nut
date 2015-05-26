from stage import *

# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }


TEMPLATE_CONTEXT_PROCESSORS += (
    # 'apps.web.contextprocessors.global.lastslug',
)


# for local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'guoku',
#         'USER': 'root',
#         'PASSWORD': 'mypass740323',
#         'HOST': 'localhost',
#         'PORT': '',
#         'OPTIONS': {
#             'use_unicode':'utf-8',
#             'init_command':'SET storage_engine=INNODB',
#         }
#     },
#     'slave': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'core',
#         'USER': 'guoku',
#         'PASSWORD': 'guoku!@#',
#         'HOST': '10.0.1.110',
#         'PORT': '',
#         'OPTIONS': {
#             'use_unicode':'utf-8',
#             'init_command':'SET storage_engine=INNODB',
#         }
#     },
# }


#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'core',
#         'USER': 'guoku',
#         'PASSWORD': 'guoku!@#',
#         'HOST': '10.0.1.110',
#         'PORT': '',
#         'OPTIONS': {
#             'use_unicode':'utf-8',
#             'init_command':'SET storage_engine=INNODB',
#         }
#     },
#     'slave': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'core',
#         'USER': 'guoku',
#         'PASSWORD': 'guoku!@#',
#         'HOST': '10.0.1.110',
#         'PORT': '',
#         'OPTIONS': {
#             'use_unicode':'utf-8',
#             'init_command':'SET storage_engine=INNODB',
#         }
#     },
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': 'guoku',
        'PASSWORD': 'guoku!@#',
        'HOST': '10.0.2.90',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
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
