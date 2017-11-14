
django_secret_key = 'zl4j09adh-*tv7-b5&(zu!nkudhry*yy1b9--$%)&yh^4caq_7'

production_master_database_name = 'core'
production_master_database_user = 'guoku'
production_master_database_pass = 'guoku!@#'
production_master_database_host = '10.0.2.90'

production_slave_database_name = 'core'
production_slave_database_user = 'guoku'
production_slave_database_pass = 'guoku!@#'
production_slave_database_host = '10.0.2.95'

test_master_database_name = 'core'
test_master_database_user = 'guoku'
test_master_database_pass = 'guoku1@#'
test_master_database_host = '10.0.2.125'

test_slave_database_name = 'core'
test_slave_database_user = 'guoku'
test_slave_database_pass = 'guoku1@#'
test_slave_database_host = '10.0.2.125'


PRODUCTION_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': production_master_database_name,
        'USER': production_master_database_user,
        'PASSWORD': production_master_database_pass,
        'HOST': production_master_database_host,
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },

    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': production_slave_database_name,
        'USER': production_slave_database_user,
        'PASSWORD': production_slave_database_pass,
        'HOST': production_slave_database_host,
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}


TESTING_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     test_master_database_name,
        'USER':     test_master_database_user,
        'PASSWORD': test_master_database_pass,
        'HOST':     test_master_database_host,
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     test_slave_database_name,
        'USER':     test_slave_database_user,
        'PASSWORD': test_slave_database_pass,
        'HOST':     test_slave_database_host,
        'PORT': '',
        'OPTIONS': {
            # 'use_unicode':'utf-8',
            'charset': 'utf8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

CELERY_RESULT_BACKEND = "redis://10.0.2.125:6379/0"
CELERY_IGNORE_RESULT = False
CELERY_TIMEZONE = 'Asia/Shanghai'
BROKER_TRANSPORT = "librabbitmq"
BROKER_HOST = "10.0.2.125"
BROKER_USER = "raspberry"
BROKER_PASSWORD = "raspberry1@#"
BROKER_VHOST = "raspberry"
BROKER_POOL_LIMIT = 10
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1




# taobao
APP_HOST = "http://www.guoku.com"
TAOBAO_APP_KEY = '12313170'
TAOBAO_APP_SECRET = '90797bd8d5859aac971f8cc9d4e51105'
# TAOBAO_APP_KEY = '23145551'
# TAOBAO_APP_SECRET = 'a6e96561f12f62515f7ed003b1652b94'
TAOBAO_OAUTH_URL = 'https://oauth.taobao.com/authorize'
TAOBAO_OAUTH_LOGOFF = 'https://oauth.taobao.com/logoff'
TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"
TAOBAO_APP_INFO = {
    "default_app_key" : "12313170",
    "default_app_secret" : "90797bd8d5859aac971f8cc9d4e51105",
    "web_app_key" : "21419640",
    "web_app_secret" : "df91464ae934bacca326450f8ade67f7"
}

BAICHUAN_APP_KEY = '23093827'
BAICHUAN_APP_SECRET = '5a9a26e067f33eea258510e3040caf17'


# weibo
SINA_APP_KEY = '2830558576'
SINA_APP_SECRET = 'a4861c4ea9facd833eb5d828794a2fb2'
# SINA_BACK_URL = APP_HOST + '/sina/auth'
SINA_BACK_URL = 'https://guoku.com/sina/auth'

# production.py will override weibo setting

# wechatfi
WECHAT_TOKEN = 'guokuinwechat'
WECHAT_APP_ID = 'wx728e94cbff8094df'
WECHAT_APP_SECRET = 'd841a90cf90d00f145ca22b82e12a500'

# jpush
JPUSH_KEY = 'f9e153a53791659b9541eb37'
JPUSH_SECRET = 'a0529d3efa544d1da51405b7'


ALIPAY_MD5_KEY = 'sij86zv335q7fb2k54iznoxg6s2z19g2'
ALIPAY_PID = '2088511535586742'
