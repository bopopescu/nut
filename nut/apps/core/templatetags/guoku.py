from django import template
from django.utils.log import getLogger

register = template.Library()
log = getLogger('django')


def enumerate_list(value):
    return enumerate(value)
register.filter(enumerate_list)


__author__ = 'edison'
