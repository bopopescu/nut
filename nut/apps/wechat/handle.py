# coding=utf-8
# from apps.wechat.models import Robots
from apps.core.models import Entity, Selection_Entity, Entity_Like
from apps.wechat.models import Token
from datetime import datetime
from django.utils.log import getLogger
from haystack.query import SearchQuerySet
from apps.wechat.robot import RobotHandler

import re

log = getLogger('django')

robot_handler = RobotHandler()

def regex(content, pattern):
    pobj = re.compile(pattern)
    return pobj.search(content.decode('utf-8'))

def handle_reply(content):
    log.error(content.decode('utf-8'))
    res = list()


    if content.decode('utf-8') == u'精选':
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)

        for row in entities[:5]:
            res.append(row.entity)
    elif content.decode('utf-8') == u'热门':
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        res = entities[:5]
    elif content.decode('utf-8') == u'合作':
        return u'合作事宜请发邮件到 bd@guoku.com'
    elif content.decode('utf-8') == u'转载':
        return u'文章转载授权请联系 alka@guoku.com'
    elif regex(content.lower(), u'平壤'):
        return u'http://www.yun-wifi.net/index.php/home/code/index/from/8'
    #     return u'「清迈旅行体验师招募｜你的工作就是玩够5天！」 ' \
    #            u'<a href="http://www.yun-wifi.net/index.php/home/code/index/from/8">►立即领抽奖码：</a>'
    elif robot_handler.can_handle(content.lower()):
        return robot_handler.handle(content.lower())
    else:
        # _entities = Entity.search.query(content.decode('utf-8')).order_by('@weight', '-created_time')
        sqs = SearchQuerySet()
        results = sqs.auto_query(content.decode('utf-8')).models(Entity).order_by('-like_count')

        for row in results[:10]:
            try:
                res.append(row.object)
            except Exception as e:
                log.error("<Error: {0}>".format(e.message))
    return res


def handle_event(content):
    # log.info(content)
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
    elif content['EventKey'] == "V2001_USER_LIKE":
        open_id = content['FromUserName']
        try:
            token = Token.objects.get(open_id=open_id)
        except Token.DoesNotExist, e:
            log.info(e)
            return None

        el = Entity_Like.objects.filter(user = token.user)
        for row in el[:5]:
            items.append(row.entity)
        # return items

    return items



__author__ = 'edison'
