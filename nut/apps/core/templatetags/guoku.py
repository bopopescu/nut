from django import template
from django.utils.log import getLogger
import time

register = template.Library()
log = getLogger('django')


def enumerate_list(value):
    return enumerate(value)
register.filter(enumerate_list)


def resize(value, size=None):
    host = 'http://imgcdn.guoku.com/'
    # host = 'http://h.guoku.com/'
    # log.info(value)
    if value is None:
        return value

    if size:
        if host in value:
            uri = value.replace(host, '')
            log.info(uri)
            params = uri.split('/')

            params.insert(1, size)
            # log.info(params)
            uri_string = '/'.join(params)
            log.info(uri_string)
            return host + uri_string
            # return "%s" % (host, params[0], params[1])
    return value
register.filter(resize)


def show_category(value):
    title = value.split('-')
    return title[0]
register.filter(show_category)


def timestamp(value):
    # log.info(type(value))
    return time.mktime(value.timetuple())
register.filter('timestamp', timestamp)

__author__ = 'edison'
