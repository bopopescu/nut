#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import re, datetime, pytz
import lxml


from Crypto.Cipher import AES
from django.utils.baseconv import base64


_RE_WEIBO = re.compile(ur'\d{1,2}')


_COVER_RE = re.compile(r'cover = "(http://.+)";')


def process_jsonp(r):
    j = r[r.find('{'):r.rfind('}')+1]
    items = json.loads(j)['items']
    l = []
    for item in items:
        root = lxml.etree.fromstring(item.replace(u'encoding="gbk"', ''))
        d = {}
        d['title'] = root.xpath('//title/text()')[0]
        d['link'] = root.xpath('//url/text()')[0]
        d['author'] = root.xpath('//sourcename/text()')[0]
        d['created'] = we_chat_date(root.xpath('//lastModified/text()')[0])
        d['guid'] = root.xpath('//docid/text()')[0]
        l.append(d)
    return l


def we_chat_date(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)) \
        .replace(tzinfo=pytz.utc).astimezone(time.timezone) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def process_content(html):
    root = lxml.html.fromstring(html)

    # 抽取封面cover图片
    script = root.xpath('//*[@id="media"]/script/text()')
    cover = None
    if script:
        l = _COVER_RE.findall(script[0])
        if l:
            cover = l[0]

    # 抽取文章内容
    try:
        content = root.xpath('//*[@id="js_content"]')[0]
    except IndexError:
        return ''

    # 处理图片链接
    for img in content.xpath('.//img'):
        if not 'src' in img.attrib:
            img.attrib['src'] = img.attrib.get('data-src', '')

    # 生成封面
    if cover:
        coverelement = lxml.etree.Element('img')
        coverelement.set('src', cover)
        content.insert(0, coverelement)

    return lxml.html.tostring(content, encoding='unicode')


def _cipher_eqs(key, secret, setting='sogou'):
    """
    SogouEncrypt.encryptquery
    """
    assert len(key) == 11

    ss = setting.split('-')

    # function g
    if len(ss) > 2:
        h = ss[2]
    else:
        h = ss[0]

    # function f
    if len(h) > 5:
        n = h[:5]
    else:
        n = h + (5 - len(h)) * 's'

    key += n

    data = secret + 'hdq=' + setting
    # padding data
    length = 16 - (len(data) % 16)
    data += chr(length) * length

    IV = b'0000000000000000'
    cipher = AES.new(_to_bytes(key), AES.MODE_CBC, IV)
    # encrypt data
    data = cipher.encrypt(_to_bytes(data))
    data = _to_unicode(base64.b64encode(data))

    # function e
    rv = ''
    i = 0
    for m in range(len(data)):
        rv += data[m]
        if (m == pow(2, i)) and i < 5:
            rv += n[i]
            i += 1
    return rv


def _to_bytes(text):
    if isinstance(text, bytes):
        return text
    return text.encode('utf-8')


def _to_unicode(text):
    if isinstance(text, str):
        return text
    return text.decode('utf-8')


def process_eqs(key, secret, setting):
    eqs = _cipher_eqs(key, secret, setting)
    return eqs
