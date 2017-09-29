# coding=utf-8

import re
import time
from datetime import datetime

from django import template
from django.utils.log import getLogger

from apps.core.models import Entity

register = template.Library()

log = getLogger('django')


def format_time(value):
    if value is None:
        return ''
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
    elif time_interval < 60 * 60 * 168:
        return "%d天前" % (time_interval / (60 * 60 * 24))
    else:
        return "%d周前" % (time_interval / (60 * 60 * 24 * 7))


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
    else:
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
    else:
        return value


register.filter(format_like_num)


def format_read_num(value):
    if value is None:
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


def find_entity_hash(raw_string):
    reg_hash = r'http://www.guoku.com/detail/(\w+)/?$'
    p = re.compile(reg_hash)
    m = p.match(raw_string)
    if m:
        return m.groups()[0]
    else:
        return None


def get_mobile_link_by_hash(hash_str):
    try:
        entity = Entity.objects.get(entity_hash=hash_str)
        return entity.mobile_url
    except Exception as e:
        return None


def mobile_link(value):
    _value = value.decode('utf-8')
    hash_str = find_entity_hash(_value)
    if hash_str:
        _value = get_mobile_link_by_hash(hash_str)
    else:
        pass

    if _value:
        _value = _value.replace('http://www.guoku.com/articles/', 'http://m.guoku.com/articles/')
        return _value.encode('utf-8')
    else:
        raise Exception('can not find link')


register.filter(mobile_link)


def at_digest(value):
    return re.sub('[\r|\n| ]', '', value)


register.filter(at_digest)

if __name__ == "__main__":
    find_entity_hash('http://127.0.0.1:9766/detail/b2836b6c')
