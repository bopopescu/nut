from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.log import getLogger

from apps.core.models import Article

log = getLogger('django')

import  re


class FeedCounterBridge(object):
    updated_feed_article_read_id_set_key = 'updated_feed_article_read_id_set'

    @classmethod
    def get_store(cls):
        return cache

    @classmethod
    def get_need_update_article_id_set(cls):
        res = cls.get_store().get(cls.updated_feed_article_read_id_set_key)
        if res is None:
            res = set()
        return res

    @classmethod
    def add_id_to_need_updated_article_id_set(cls, id):
        theSet = cls.get_need_update_article_id_set()
        theSet.add(id)
        cls.get_store().set(cls.updated_feed_article_read_id_set_key, theSet, timeout=None)
        return

    @classmethod
    def clear_need_update_article_id_set(cls):
        cls.get_store().set(cls.updated_feed_article_read_id_set_key, set(), timeout=None)
        return

    @classmethod
    def get_feed_count_value_from_sql(cls, id):
        article = Article.objects.get(pk=id)
        return article.feed_read_count or 1

    @classmethod
    def save_feed_count_value_to_sql(cls, id, count):
        article = Article.objects.get(pk=id)
        article.feed_read_count = count
        return

    @classmethod
    def get_article_feed_read_count_key(cls, article_id):
        return 'feed_article_read_count_%s' % article_id

    @classmethod
    def get_article_feed_read_count(cls, id):
        key = cls.get_article_feed_read_count_key(id)
        try :
            count = cls.get_store().get(key)
        except ValueError:
            try :
                count = cls.get_feed_count_value_from_sql(id)
            except Exception as e:
                count = 1

        return count

    @classmethod
    def incr_article_feed_read_count(cls, id):
        key = cls.get_article_feed_read_count_key(id)
        counter_store = cls.get_store()
        try :
            counter_store.incr(key)
        except ValueError:
            try :
                count = cls.get_feed_count_value_from_sql(id)
            except Exception as e:
                count = 1
            counter_store.set(key, count, timeout=None)

        except Exception as e:
            raise CounterException('image counter error')

        cls.add_id_to_need_updated_article_id_set(id)
        return


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
    def set_article_read_count_from_pk(cls,pk,count):
        path = reverse('web_article_page', args=[pk])
        key = cls.get_counter_key_from_path(path)
        counter_store = cls.get_store()
        key = cls._hash_key(key)
        res = counter_store.set(key, count ,timeout=None)
        return res

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
            try:
                count  = cls.get_count_value_from_mysql_by_key(key)
            except Exception as e :
                count = 1
            counter_store.set(key, count ,timeout=None)
            return count
        except Exception as e :
            raise CounterException(' increment error %s' %e.message)
        return count

    @classmethod
    def get_count_value_from_mysql_by_key(cls,key):
        pk = cls.get_article_pk_from_counter_key(key)
        article = Article.objects.get(pk=pk)
        if article.read_count is None:
            return 1
        else:
            return article.read_count

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
            return res
        # return res27
