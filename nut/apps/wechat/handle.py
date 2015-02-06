from apps.wechat.models import Robots
from apps.core.models import Entity
import json

from django.utils.log import getLogger

log = getLogger('django')


def handle_reply(content):
    _entities = Entity.search.query(content).order_by('@weight', '-created_time')
    # log.info(_entities.all())
    # for row in _entities.all():
    #     log.info(row)
    res = list()
    for row in _entities.all():
        res.append(row)
    # log.info(res)
    return res
    # _item = Robots.objects.filter(accept__contains=content).first()
    #
    # if _item is None:
    #     return None
    #
    # # res = {}
    # if _item.type == Robots.news:
    #     # log.info(_item.content)
    #     _content = json.loads(_item.content)
    #     # log.info(type(_content))
    #     log.info(type(_item.content))
    #     res = {
    #         'type': _item.get_type_display,
    #         'title': _content['title'],
    #         'picurl': _content['picurl'],
    #         'url': _content['url'],
    #     }
    #     log.info(res)
    # else:
    #     res = {
    #         'type':_item.get_type_display,
    #         'content': _item.content
    #     }
    # return res


__author__ = 'edison'
