#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.fetch.amazon import Amazon
from apps.fetch.jd import JD
from apps.fetch.kaola import Kaola
from apps.fetch.six_pm import SixPM
from apps.fetch.taobao import TaoBao
from apps.fetch.tmall import Tmall
from apps.fetch.booking import Booking

spider_map = {
    'jd': JD,
    '360buy': JD,
    'taobao': TaoBao,
    '95095': TaoBao,
    'yao': TaoBao,
    'tmall': Tmall,
    'amazon': Amazon,
    'kaola': Kaola,
    'booking': Booking,
    '6pm': SixPM
}
