import hashlib
import redis
from urlparse import urlparse

from django.conf import settings
from django.views.generic import View
from django_redis import get_redis_connection

from braces.views import JSONResponseMixin, AjaxResponseMixin

from django.utils.log import getLogger
log = getLogger('django')

from apps.counter.utils.data import RedisCounterMachine, CounterException

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
        except CounterException as e:
            return self.response_error_message(e.message)

        try:
            count = RedisCounterMachine.increment_key(counter_key)
        except CounterException as e:
            return self.response_error_message(e.message)

        res = {
            'count':count,
        }
        return self.response_sucess_obj(res)