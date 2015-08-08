from django import template
from django.utils.log import getLogger
from django.conf import settings

import time
import qrcode
import StringIO
# import base64


register = template.Library()
log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)

def enumerate_list(value):
    return enumerate(value)
register.filter(enumerate_list)


def resize(value, size=None):
<<<<<<< HEAD
    host = image_host
    # log.info(value)
    # host = 'http://h.guoku.com/'
    if value is None or host not in value:
        return value

    if size:
        if host in value:
            uri = value.replace(host, '')
            # log.info(uri)
=======
    # for local debug.
    hosts = [image_host, 'http://imgcdn.guoku.com/']
    for h in hosts:
        if h in value:
            uri = value.replace(h, '')
>>>>>>> 94e00b1c74ab6d8c944e41174a8216195115287c
            params = uri.split('/')
            params.insert(1, size)
            uri_string = '/'.join(params)
<<<<<<< HEAD
            # print uri_string
            # return 'http://image.guoku.com/' + uri_string
            return host + uri_string
=======
            return h + uri_string
            break
>>>>>>> 94e00b1c74ab6d8c944e41174a8216195115287c

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

def entity_qr(value):
    url = "%s%s" % ('http://www.guoku.com', value)
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=1,
    )
    qr.add_data(url)
    img = qr.make_image()
    # content = img.convert('RGBA').tostring("raw", "RGBA")
    output = StringIO.StringIO()
    #
    img.save(output)
    # # log.info(output.getvalue())
    content = output.getvalue()
    output.close()
    # log.info(content)
    # output.close()
    return content.encode('base64').replace("\n", "")
register.filter(entity_qr)





__author__ = 'edison'
