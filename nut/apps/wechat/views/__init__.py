from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.conf import settings

import hashlib

TOKEN = getattr(settings, 'WeChatToken', 'guokuinwechat')


class WeChatView(View):
    token = TOKEN

    def validate(self, request):
        _signature = request.REQUEST.get('signature', None)
        _timestamp = request.REQUEST.get('timestamp', None)
        _nonce = request.REQUEST.get('nonce', None)

        list = [self.token, _timestamp, _nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        if hashcode == _signature:
            return True
        return False

    def get(self, request):
        if self.validate(request):
            echostr = request.GET.get('echostr', None)
            return HttpResponse(echostr)
        raise PermissionDenied

__author__ = 'edison'
