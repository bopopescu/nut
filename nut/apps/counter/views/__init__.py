from urlparse import urlparse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.cache import cache
from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.utils.log import getLogger

from apps.counter.utils.data import RedisCounterMachine, FeedCounterBridge


log = getLogger('django')

class Counter(JSONResponseMixin, AjaxResponseMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Counter, self).dispatch(request, *args, **kwargs)

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
        # referer = request.META['HTTP_REFERER']
        path = request.POST.get('counter_path')
        # path =  urlparse(referer).path
        return RedisCounterMachine.get_counter_key_from_path(path)

    def post(self, request, *args, **kwargs):
        return self.post_ajax(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        counter_key = None
        try:
            counter_key = self.get_key(request)
            article_pk = RedisCounterMachine.get_article_pk_from_counter_key(counter_key)
            RedisCounterMachine.add_need_update_article_id(article_pk)
        except Exception as e:
            return self.response_error_message(e.message)

        try:
            count = RedisCounterMachine.increment_key(counter_key)
        except Exception as e:
            return self.response_error_message(e.message)

        res = {
            'count': count,
        }
        return self.response_sucess_obj(res)


class ArticleImageCounter(View):

    def __init__(self):
        self.feedCounterBridge = FeedCounterBridge()

    def get_img_data(self):
        img_key = 'guoku_counter_image_key_2016'
        img_data = cache.get(img_key)
        if img_data:
            return img_data
        else:
           img_data = open('static/images/guoku_banner_2016.jpg').read()
           cache.set(img_key, img_data, timeout=60*60*24)
           return img_data

    def updateCounter(self, id):
        self.feedCounterBridge.incr_article_feed_read_count(id)

    def get(self, *args ,**kwargs):
        id = self.kwargs.pop("aid")
        img_data = self.get_img_data()
        try :
            self.updateCounter(id)
        except Exception as e :
            pass
        return HttpResponse(img_data, content_type='image/jpeg')




