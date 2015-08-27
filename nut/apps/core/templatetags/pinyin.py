from django import template
from django.utils.log import getLogger
# from django.conf import settings
from xpinyin import Pinyin

register = template.Library()
log = getLogger('django')


def pinyin(value):
    p = Pinyin()
    return p.get_pinyin(value, '')
    # log.info(res)
    # return res
register.filter(pinyin)

__author__ = 'xiejiaxin'
