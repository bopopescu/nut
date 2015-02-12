# coding=utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.core.exceptions import PermissionDenied
from django.views.generic import View,CreateView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.log import getLogger
from datetime import datetime
import time
from xml.etree import ElementTree as ET
import hashlib

# from apps.wechat.models import Robots
from apps.wechat.handle import handle_reply
TOKEN = getattr(settings, 'WeChatToken', 'guokuinwechat')

log = getLogger('django')


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

    def parseMsgXml(self, rootElem):

        msg = {}
        if rootElem.tag == 'xml':
            for child in rootElem:
                msg[child.tag] = smart_str(child.text)
        return msg


    def get(self, request):
        if self.validate(request):
            echostr = request.GET.get('echostr', None)
            return HttpResponse(echostr)
        raise PermissionDenied

    def post(self, request):
        # log.info(request.body)
        rawStr = request.body
        # log.info(rawStr)
        if self.validate(request):
            msg = self.parseMsgXml(ET.fromstring(rawStr))
            log.info(msg)
            _timestamp = time.mktime(datetime.now().timetuple())
            log.info(_timestamp)
            # _items = Robots.objects.filter(accept__contains=msg['Content']).first()
            if msg['MsgType'] == 'voice':
                _items = handle_reply(msg['Recognition'])
            else:
                _items = handle_reply(msg['Content'])
            log.info(_items[:5])
            return render_to_response(
                'wechat/reply.xml',
                {
                    'msg': msg,
                    # 'item': _item,
                    'items': _items[:5],
                    'timestamp': int(_timestamp),
                },
                mimetype="application/xml",
            )

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WeChatView, self).dispatch(request, *args, **kwargs)

__author__ = 'edison'
