from urlparse import urlparse
from django.http import HttpResponse
from django.views.generic import View

from django.core.cache import cache

from braces.views import JSONResponseMixin, AjaxResponseMixin

from django.utils.log import getLogger
log = getLogger('django')

from apps.counter.utils.data import RedisCounterMachine, CounterException
from abc import ABCMeta, abstractmethod

class Counter(JSONResponseMixin, AjaxResponseMixin, View):

    def get(self, request):
        # dummy :)
        return self.render_json_response({
            'name':'ant'
        })

    def response_error_message(self, message):
        res = {
            'error':1,
            'message':message
        }
        return self.render_json_response(res)
    def response_sucess_obj(self, obj):
        res = {
            'error': 0,
        }
        res.update(obj)
        return self.render_json_response(res)

    def get_key(self, request):
        referer = request.META['HTTP_REFERER']
        path =  urlparse(referer).path
        return  RedisCounterMachine.get_counter_key_from_path(path)

    def get_ajax(self, request , *args, **kwargs):
        counter_key = None
        try:
            counter_key = self.get_key(request)
        except Exception as e:
            return self.response_error_message(e.message)

        try:
            count = RedisCounterMachine.increment_key(counter_key)
        except Exception as e:
            return self.response_error_message(e.message)

        res = {
            'count':count,
        }
        return self.response_sucess_obj(res)



class CounterView(View):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_couter_key(self):
        pass

    @abstractmethod
    def get_store(self):
        pass

    @abstractmethod
    def incr_key(self , key ):
        store = self.get_store()
        store.incr(key)
        pass

    @abstractmethod
    def get_key_from_mysql(self, key):
        pass


class ArticleImageCounter(CounterView):
    def get_img_data(self):
        img_key = 'guoku_counter_image_key'
        img_data  = cache.get(img_key)
        if img_data:
            return img_data
        else:
           img_data = open('static/images/guoku_banner.jpg').read()
           cache.set(img_key, img_data, timeout=60*60*24)
           return img_data

    def updateCounter(self,id):

        return

    def get(self, *args ,**kwargs):
        id = self.kwargs.pop("aid")
        img_data = self.get_img_data()
        self.updateCounter(id)
        return HttpResponse(img_data, content_type='image/jpeg')




