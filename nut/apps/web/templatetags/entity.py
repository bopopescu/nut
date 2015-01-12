# coding=utf-8
from django.utils.log import getLogger
from django import template

register = template.Library()
log = getLogger('django')



# def trans_category(value):
#     _category_context = Category(value).read()
#     log.info(_category_context)
#     _title = _category_context['category_title'].split('-')[0]
#     return _title
# register.filter('trans_category', trans_category)


__author__ = 'edison'
