#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from apps.core.fetch import get_origin_source_by_url, clean_price_string
from apps.core.fetch.amazon import Amazon
from apps.core.fetch.booking import Booking
from apps.core.fetch.jd import JD
from apps.core.fetch.kaola import Kaola
from apps.core.fetch.six_pm import SixPM
from apps.core.fetch.spider import get_provider
from apps.core.fetch.taobao import TaoBao
from apps.core.fetch.tmall import Tmall


@pytest.mark.parametrize('provider,hostname,key', (
        (TaoBao, 'taobao.com', 'taobao'),
        (Tmall, 'tmall.com', 'tmall'),
        (JD, 'jd.com', 'jd'),
        (Kaola, 'kaola.com', 'kaola'),
        (Booking, 'booking.com', 'booking'),
        (SixPM, '6pm.com', '6pm'),
        (TaoBao, 'yao.95095.com', '95095'),
        (Amazon, 'amazon.cn', 'amazon_cn'),
        (Amazon, 'amazon.com', 'amazon_com'),
))
def test_get_provider_and_source(provider, hostname, key, links):
    for link in links[key].keys():
        assert get_origin_source_by_url(link) == hostname
        assert get_provider(link) == provider


def test_get_origin_source_by_url():
    test_url = 'http://www.baidu.com'
    assert get_origin_source_by_url(test_url) == 'baidu.com'
    assert get_provider(test_url) is None

    test_url = 'http://www.weibo.com'
    assert get_origin_source_by_url(test_url) == 'weibo.com'
    assert get_provider(test_url) is None

    test_url = 'http://www.ele.me'
    assert get_origin_source_by_url(test_url) == 'ele.me'
    assert get_provider(test_url) is None


def test_clean_price_string():
    assert clean_price_string(u'$ 56 - 89') == 56.00
    assert clean_price_string(u'￥ 59.00 ') == 59.00
    assert clean_price_string(u'￥50.00 - 238.00') == 50.00
    assert clean_price_string(u'9999') == 9999
    assert clean_price_string(u'flkdsjfewn') is None
