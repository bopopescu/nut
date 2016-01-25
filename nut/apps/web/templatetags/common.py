# coding=utf-8

from django import template
# from django.conf import settings
from django.utils.log import getLogger
from datetime import datetime
from apps.tag.models import Tags, Content_Tags
from apps.core.models import Entity
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
            return "<p class='boolean-true'>是</p>"
        else :
            return "<p class='boolean-false'>否</p>"
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
        tag_string = article.tags_string
        return tag_string
register.filter(article_tag_string)


def find_entity_hash(str):
    regHash = r'http://www.guoku.com/detail/(\w+)/?$'
    p  = re.compile(regHash)
    m = p.match(str)
    if m :
        return  m.groups()[0]
    else:
        return None

def get_mobile_link_by_hash(theHash):
    try:
        entity = Entity.objects.get(entity_hash=theHash)
        return entity.mobile_url
    except Exception as e:
        return None
    return

def mobile_link(value):
   _value = value.decode('utf-8')
   theHash = find_entity_hash(_value)
   if theHash:
        _value = get_mobile_link_by_hash(theHash)
   else:
       pass

   if _value :
        _value = _value.replace('http://www.guoku.com/articles/','http://m.guoku.com/articles/')
        return _value.encode('utf-8')
   else :
       raise Exception('can not find link')
register.filter(mobile_link)




if __name__ == "__main__":
    find_entity_hash('http://127.0.0.1:9766/detail/b2836b6c')

__author__ = 'edison7500'
