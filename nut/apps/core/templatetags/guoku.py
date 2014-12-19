from django import template
from django.utils.log import getLogger

register = template.Library()
log = getLogger('django')


def enumerate_list(value):
    return enumerate(value)
register.filter(enumerate_list)


def resize(value, size=None):
    host = 'http://imgcdn.guoku.com/'
    # host = 'http://h.guoku.com/'
    log.info(value)
    if size:
        if host in value:
            uri = value.replace(host, '')
            log.info(uri)
            params = uri.split('/')

            params.insert(1, size)
            # log.info(params)
            uri_string = '/'.join(params)
            log.info(uri_string)
            return "http://h.guoku.com/" + uri_string
            # return "%s" % (host, params[0], params[1])
    return value
register.filter(resize)
__author__ = 'edison'
