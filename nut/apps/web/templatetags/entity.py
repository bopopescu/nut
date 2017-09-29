# coding=utf-8
from django.utils.log import getLogger
from django import template

register = template.Library()
log = getLogger('django')
