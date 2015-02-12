# coding=utf-8
# from apps.wechat.models import Robots
from apps.core.models import Entity, Selection_Entity, Entity_Like
from datetime import datetime
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


def handle_event(content):
    log.info(content)
    items = []
    if content['EventKey'] == "V1001_SELECTION":
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)

        for row in entities[:5]:
            items.append(row.entity)
        # return items
    elif content['EventKey'] == "V1002_POPULAR":
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        items = entities[:5]
        # items = entities[:5]
    return items

__author__ = 'edison'
