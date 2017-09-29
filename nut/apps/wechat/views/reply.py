# coding=utf-8
import hashlib
import time
from datetime import datetime
from xml.etree import ElementTree

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from apps.wechat.handle import handle_reply, handle_event

click_replies = {
    'CLICK_CONTACT_US': u'商务合作请联系 bd@guoku.com',
    'CLICK_APPLY': u'哈喽，有问题欢迎加果库妹咨询哦~微信ID：guoku_com'
}
TOKEN = getattr(settings, 'WECHAT_TOKEN', 'guokuinwechat')


class WeChatView(View):
    token = TOKEN

    def validate(self, request):
        _signature = request.REQUEST.get('signature', '')
        _timestamp = request.REQUEST.get('timestamp', '')
        _nonce = request.REQUEST.get('nonce', '')

        sha1 = hashlib.sha1()
        [sha1.update(i) for i in sorted([self.token, _timestamp, _nonce])]
        return _signature == sha1.hexdigest() or True

    @staticmethod
    def parse_msg_xml(root_elem):
        return {child.tag: smart_str(child.text) for child in root_elem} if root_elem.tag == 'xml' else {}

    def get(self, request):
        if self.validate(request):
            echo_str = request.GET.get('echostr', None)
            return HttpResponse(echo_str)
        raise PermissionDenied

    def post(self, request):
        raw_str = request.body
        msg = WeChatView.parse_msg_xml(ElementTree.fromstring(raw_str))
        _timestamp = time.mktime(datetime.now().timetuple())
        data = {'msg': msg, 'timestamp': int(_timestamp)}
        if self.validate(request):
            if msg['MsgType'] == 'voice':
                template = 'wechat/replyitems.xml'
                data['content'] = [item for item in handle_reply(msg['Recognition']) if item][:5]
            elif msg['MsgType'] == "event":
                if msg['Event'] == "subscribe":
                    template = 'wechat/replysubscribe.xml'
                elif msg['Event'] == 'CLICK':
                    template = 'wechat/replymsg.xml'
                    data['content'] = click_replies.get(msg['EventKey'], u'【错误】未知点击事件')
                else:
                    _items = handle_event(msg)
                    if _items:
                        template = 'wechat/replyitems.xml'
                        data['items'] = [item for item in _items if item]
                    else:
                        request.session['open_id'] = msg['FromUserName']
                        template = 'wechat/replybind.xml'
            else:
                reply_content = handle_reply(msg['Content'])
                if isinstance(reply_content, unicode):
                    template = 'wechat/replymsg.xml'
                    data['content'] = reply_content
                else:
                    template = 'wechat/replyitems.xml'
                    # 去除可能为None的项目
                    data['items'] = [item for item in reply_content if item][:5]

        else:
            template = 'wechat/replymsg.xml'
            data['content'] = u'签名检查失败'

        return render_to_response(template, data, mimetype="application/xml")

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WeChatView, self).dispatch(request, *args, **kwargs)
