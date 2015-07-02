from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
log = getLogger('django')

import  re

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
    def get_store(cls):
        return cache

    @classmethod
    def _hash_key(cls,key):
        # do not hash key , use them directly
        # return  hashlib.sha1(key).hexdigest()
        return key
    @classmethod
    def get_counter_key_from_path(cls, path):
        prefix = 'counter'
        key_body = ':'.join(path.split('/'))
        return '%s%s'%(prefix, key_body)

    @classmethod
    def get_article_read_count_key_from_pk(cls,pk):
        path = reverse('web_article_page', args=[pk])
        return cls.get_counter_key_from_path(path)

    @classmethod
    def get_article_pk_from_counter_key(cls, key):
        matchs = re.findall("counter:articles:(\d+):", key)
        if matchs :
            return long(matchs[0])
        else:
            return None

    @classmethod
    def get_read_counts(cls,articles):
        keys = [cls.get_article_read_count_key_from_pk(article.pk) for article in articles]
        res = cls.get_keys_count(keys)
        final_res = dict()
        for key  in res:
            final_res[cls.get_article_pk_from_counter_key(key)] =res[key]

        return final_res
        # return dict(zip(pks,counts));

    @classmethod
    def increment_key(cls,key):
        counter_store = cls.get_store()
        key = cls._hash_key(key)
        try :

            count = counter_store.incr(key)
        except ValueError :
            # cache this value forever
            counter_store.set(key, 1, timeout=None)
            count = 1
            return count
        except Exception as e :
            raise CounterException(' increment error %s' %e.message)
        return count

    @classmethod
    def get_key(cls,key):
        r_server= cls.get_store()
        hkey = cls._hash_key()
        try:
            value = r_server.get(hkey)
        except:
            raise  CounterException('can not get key ')
        return value

    @classmethod
    def get_keys_count(cls, keys):
        r_server = cls.get_store()
        hashed_keys = [cls._hash_key(key) for key in keys]
        res = None
        try:
            res = r_server.get_many(hashed_keys)
            # return res
        except :
            raise CounterException('can not mget keys ')
        finally:
<<<<<<< HEAD
            return res
        # return res
=======
            return res
>>>>>>> f5cc7fb016b898ae36e26601b6a190c9940a8d27
