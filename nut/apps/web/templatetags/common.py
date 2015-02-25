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

    if time_interval < 60:
        return "%d 秒前" % (time_interval)
    elif time_interval < 60 * 60:
        return "%d 分钟前" % ((time_interval / 60) + 1)
    elif time_interval < 60 * 60 * 24:
        return "%d 小时前" % (time_interval / (60 * 60) + 1)
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    return "%d 年 %d 月 %d 日" % (value.year, value.month, value.day)

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

__author__ = 'edison7500'
