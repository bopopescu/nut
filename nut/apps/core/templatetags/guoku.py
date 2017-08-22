# coding=utf-8
from django import template
from django.utils.log import getLogger
from django.conf import settings

import time
import qrcode
import StringIO
import bleach

ALLOWED_NOTE_TAGS = []

register = template.Library()
log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)


def enumerate_list(value):
    return enumerate(value)


register.filter(enumerate_list)


def smart_scheme(value, is_secure=False):
    if not is_secure:
        return value
    else:
        return value.replace('http://', 'https://')


register.filter(smart_scheme)


def safe_note(value):
    return bleach.clean(value, tags=ALLOWED_NOTE_TAGS)


register.filter(safe_note)


def https_image_cdn(value):
    http_host = settings.IMAGE_HOST
    https_host = http_host.replace('http://', 'https://')
    return value.replace(http_host, https_host)


register.filter(https_image_cdn)


def oss_resize(url, size=None):
    if all([url, size]):
        if 'taobaocdn.com' in url or 'alicdn.com' in url:
            # 淘宝地址，修改到淘宝规则的地址
            url = '{url}_{size}x{size}.jpg'.format(url=url, size=size)

        elif image_host in url:
            # CDN地址，修改到阿里云规则的地址
            url = '{value}/{size}'.format(value=url, size=size)

    url = url.replace('//images', '/images')
    return url


register.filter(oss_resize)


def resize(value, size=None):
    host = image_host
    if value is None:
        return value

    if 'taobaocdn.com' in value or 'alicdn.com' in value:
        value = value + '_' + size + 'x' + size + '.jpg'
        return value

    if 'guoku.com/static' in value:
        return value

    if host not in value:
        return value

    if size:
        if host in value:
            uri = value.replace(host, '')
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
    return time.mktime(value.timetuple())


register.filter('timestamp', timestamp)


def filter_builder(filter_name, filter_value):
    return '%s=%s' % (filter_name, filter_value)


register.filter('filter_builder', filter_builder)


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
    output = StringIO.StringIO()
    img.save(output)
    content = output.getvalue()
    output.close()
    return content.encode('base64').replace("\n", "")


register.filter(entity_qr)


def tbsearch_url(word):
    return 'https://s.taobao.com/search?q=%s' % word


register.filter(tbsearch_url)
