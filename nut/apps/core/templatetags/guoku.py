from django import template
from django.utils.log import getLogger
from django.conf import settings

# import hashlib
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
    host = image_host
    # log.info(value)
    if value is None:
        return value

    if 'taobaocdn.com' in value or 'alicdn.com' in value:
        value = value+'_'+size+'x'+size+'.jpg'
        return value

    if host not in value:
        return value

    if size:
        if host in value:
            uri = value.replace(host, '')
            # log.info(uri)
            params = uri.split('/')
            params.insert(1, str(size))
            uri_string = '/'.join(params)
            return host + uri_string

    value = value.replace('//images', '/images')
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

def filter_builder(filter_name, filter_value):
    return '%s=%s' %(filter_name, filter_value)
register.filter('filter_builder',filter_builder )


# deprecate !! performance hitter
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

#
# # deprecated
# def qrimg(url):
#     return 'deprecated'
#     # return get_qrcode_img_url(url)
# register.filter(qrimg)







__author__ = 'edison'
