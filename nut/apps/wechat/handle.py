from apps.wechat.models import Robots
import json

from django.utils.log import getLogger

log = getLogger('django')


def handle_reply(content):

    _item = Robots.objects.filter(accept__contains=content).first()

    res = {}
    if _item.type == Robots.news:
        # log.info(_item.content)
        _content = json.loads(_item.content)
        # log.info(type(_content))
        log.info(type(_item.content))
        res = {
            'type': _item.get_type_display,
            'title': _content['title'],
            'picurl': _content['picurl'],
            'url': _content['url'],
        }
        log.info(res)
    else:
        res = {
            'type':_item.get_type_display,
            'content': _item.content
        }
    return res


__author__ = 'edison'
