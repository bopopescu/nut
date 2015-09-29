# coding=utf-8

from django import template
# from django.conf import settings
from django.utils.log import getLogger
from datetime import datetime
from apps.tag.models import Tags, Content_Tags
import time
import re


register = template.Library()

log = getLogger('django')

def format_time(value):
    if type(value) is str:
        return value
    before_time = time.mktime(value.timetuple())
    now = time.mktime(datetime.now().timetuple())
    time_interval = now - before_time

    if time_interval < 0:
        return "刚刚"
    elif time_interval < 60:
        return "%d秒前" % time_interval
    elif time_interval < 60 * 60:
        return "%d分钟前" % ((time_interval / 60) + 1)
    elif time_interval < 60 * 60 * 24:
        return "%d小时前" % (time_interval / (60 * 60))
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    elif time_interval < 60*60*168:
        return "%d天前"%(time_interval/(60*60*24))
    else:
        return "%d周前"%(time_interval/(60*60*24*7))
    # NEVER GO HERE
    return "很久很久以前"

register.filter(format_time)

def selection_previous_paginator(value):
    if value % 3 == 0:
        value -= 2
    return value
register.filter(selection_previous_paginator)

def selection_next_paginator(value):
    if value % 3 == 2:
        value += 2

    return value
register.filter(selection_next_paginator)


def format_boolean(value):
        if value:
            return "是"
        else :
            return "否"
register.filter(format_boolean)

def format_boolean_class(value):
    if value:
        return 'bool_yes'
    else:
        return 'bool_no'

register.filter(format_boolean_class)

def format_like_num(value):

    if value == 0:
        return 1
    else :
        return value
register.filter(format_like_num)

def format_read_num(value):
    if  value is None:
        return '0'
    else:
        return value

register.filter(format_read_num)

def trim(value):
    return value.strip()
register.filter(trim)

def maybe_none(value):
    if value is None:
        return ''
    else:
        return value
register.filter(maybe_none)

def handle_brand_intro(value):
    if value is None:
        return ''
    else:
        value = value.replace('\n', '<br>')
    return value
register.filter(handle_brand_intro)


def article_tag_string(article):
        tids = Content_Tags.objects.filter(target_content_type=31, target_object_id=article.pk).values_list('tag_id', flat=True)
        tags = Tags.objects.filter(pk__in=tids)
        tag_list=[]
        for row in tags:
            tag_list.append(row.name)
        tag_string = ",".join(tag_list)
        return tag_string
register.filter(article_tag_string)


def find_entity_hash(str):
    theHash = ''
    regHash = r'http://www.guoku.com/detail/(\w+)/?$'
    p  = re.compile(regHash)
    m = p.match(str)
    if m :
        print m.group()
    else:
        print 'not found'

    return theHash

def mobile_link(value):
   _value = value.decode('utf-8')

   _value = _value.replace('http://www.guoku.com/detail/', 'guoku://entity/')
   _value = _value.replace('http://www.guoku.com/articles/','http://m.guoku.com/articles/')
   return _value.encode('utf-8')
register.filter(mobile_link)

if __name__ == "__main__":
    find_entity_hash('http://127.0.0.1:9766/detail/b2836b6c')

__author__ = 'edison7500'
