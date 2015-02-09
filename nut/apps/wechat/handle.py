# coding=utf-8
# from apps.wechat.models import Robots
from apps.core.models import Entity

from django.utils.log import getLogger

log = getLogger('django')


def handle_reply(content):
    # log.info(content.decode('utf-8'))
    _entities = Entity.search.query(content.decode('utf-8')).order_by('@weight', '-created_time')
    # log.info(_entities.all())
    # for row in _entities.all():
    #     log.info(row)
    res = list()
    for row in _entities.all():
        res.append(row)
    log.info(res)
    return res


__author__ = 'edison'
