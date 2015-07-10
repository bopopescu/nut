# coding=utf-8

from django import template
# from django.conf import settings
from django.utils.log import getLogger
from datetime import datetime
import time


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
        return "%d小时前" % (time_interval / (60 * 60) + 1)
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    elif time_interval < 60*60*168:
        return "%d天前"%(time_interval/(60*60*24) + 1)
    else:
        return "%d周前"%(time_interval/(60*60*24*7) + 1)
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
        return ''
    else :
        return value
register.filter(format_like_num)

def format_read_num(value):
    if  value is None:
        return '0'
    else:
        return value

register.filter(format_read_num)


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

__author__ = 'edison7500'
