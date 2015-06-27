
from django.conf import settings


from django.views.generic import View
from django_redis import get_redis_connection

from braces.views import JSONResponseMixin, AjaxResponseMixin

from urlparse import urlparse
import hashlib
import redis


class Counter(JSONResponseMixin, AjaxResponseMixin, View):

    def get_redis_server(self):
        r_server = None
        if settings.LOCAL_TEST_ANT:
            r_server = redis.Redis(settings.LOCAL_REDIS_SERVER)
        else:
            try :
               r_server = get_redis_connection("default")
            except:
                raise Exception('can not find redis server')
        return r_server


    def get(self, request):
        return self.render_json_response({
            'name':'ant'
        })

    def get_ajax(self, request , *args, **kwargs):
        referer = request.META['HTTP_REFERER']
        path =  urlparse(referer).path
        r_server = None
        if path :
            key = hashlib.sha1(path).hexdigest()
        else:
            res ={
                'error':1,
                'message':'can not get referral path',
            }
            return self.render_json_response(res)

        try:
            r_server = self.get_redis_server()
        except Exception as e:
            res={
                'error':1,
                'message': 'can not connect redis server'
            }
            return self.render_json_response(res)


        #  TODO : go on for counter


        return self.render_json_response({
            'name':'clara'
        })