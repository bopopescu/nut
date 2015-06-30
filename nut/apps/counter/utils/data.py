import hashlib
import redis
from django.conf import settings
from django_redis import get_redis_connection
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
log = getLogger('django')


class CounterException(Exception):
    pass

class RedisCounterMachine(object):
    '''
        A class for web static/counter util
        to provide a middle layer of 1. connection/accessing redis server
                                     2. handle key hash
                                     3. handle group get generate and get
                                     4.
    '''

    @classmethod
    def get_redis_server(cls):
        r_server = None
        try :
            if hasattr(settings ,'LOCAL_TEST_REDIS'):
                # no need for pooling, for local test
                r_server = redis.Redis(settings.LOCAL_TEST_REDIS_HOST)
            elif hasattr(settings, 'TEST_SERVER_REDIS'):
                # test.guoku.com
                r_server = redis.Redis(settings.TEST_SERVER_REDIS_HOST)
            elif hasattr(settings, 'PRODUCTION_REDIS_SERVER'):
                log.error('anchen: connecting redis %s '%settings.PRODUCTION_REDIS_SERVER_HOST)
                r_server = redis.Redis(settings.PRODUCTION_REDIS_SERVER_HOST)
            else:
                log.error('anchen: not setting for connection redis')
                raise  CounterException('can not find redis settings')
        except Exception as e:
            log.error('anchen: exception when get server %s'%e.message)
            raise CounterException('can not find redis server, for :%s', e.message)
        return r_server

    @classmethod
    def _hash_key(cls,key):
        # do not hash key , use them directly
        # return  hashlib.sha1(key).hexdigest()
        return key
    @classmethod
    def get_counter_key_from_path(cls, path):
        prefix = 'counter'
        key_body = ':'.join(path.split('/'))
        log.error('key generated ')
        log.error('%s%s'%(prefix, key_body))
        return '%s%s'%(prefix, key_body)

    @classmethod
    def get_article_read_count_key_from_pk(cls,pk):
        path = reverse('web_article_page', args=[pk])
        return cls.get_counter_key_from_path(path)

    @classmethod
    def get_read_counts(cls,articles):
        pks  = [article.pk for article in articles]
        keys = [cls.get_article_read_count_key_from_pk(article.pk) \
                for article in articles]
        counts = cls.get_keys_count(keys)
        return dict(zip(pks,counts));


    @classmethod
    def increment_key(cls,key):
        r_server = cls.get_redis_server()
        key = cls._hash_key(key)
        try :

            count = r_server.incr(key)
            log.error('key incremented for key %s'%key)
        except :
            raise CounterException('can not ')
        return count

    @classmethod
    def get_key(cls,key):
        r_server= cls.get_redis_server()
        hkey = cls._hash_key()
        try:
            value = r_server.get(hkey)
        except:
            raise  CounterException('can not get key ')
        return value


    @classmethod
    def get_keys_count(cls, keys):
        r_server = cls.get_redis_server()
        hashed_keys = [cls._hash_key(key) for key in keys]
        try:
            res = r_server.mget(*hashed_keys)
        except :
            raise CounterException('can not mget keys ')
        return res