#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.core.fetch import get_origin_source_by_url


def test_parse_amazon_id_from_url():
    pass


def test_parse_taobao_id_from_url():
    pass


def test_parse_jd_id_from_url():
    pass


def test_parse_kaola_id_from_url():
    pass


def test_parse_booking_id_from_url():
    pass


def test_get_key():
    pass


def test_get_origin_id_by_url():
    pass


def test_get_origin_source_by_url():
    taobao_links = ('https://item.taobao.com/item.htm?spm=a21bo.7724922.8446.2.oi90zh&scm=1007.10325.17076.0&id=43352358270',
                    'https://item.taobao.com/item.htm?spm=5704.2075955.1998837601.98.GHug7u&id=522087255299',
                    'https://item.taobao.com/item.htm?spm=a219e.7778345.24768.9.oIZ6TF&id=37353406383',
                    'https://detail.tmall.com/item.htm?spm=a230r.1.14.51.hQrvPf&id=21361619524&ns=1&_u=hfgvk8386d7&abbucket=8',
                    )
    for link in taobao_links:
        assert get_origin_source_by_url(link) == 'taobao.com'

    jd_links = ('http://item.jd.com/880516.html',
                'http://item.jd.com/234579.html',
                'http://item.jd.com/1090086.html',
                )
    for link in jd_links:
        assert get_origin_source_by_url(link) == 'jd.com'

    tmall_links = ('https://detail.tmall.com/item.htm?spm=a1z10.5-b.w4011-6947701451.28.gkW48M&id=524854465546&rn=28e1186d09057bfe346db810d1baafbe&abbucket=17',
                   'https://detail.tmall.com/item.htm?id=524204082213&spm=a1z0k.7385961.1997985097.d4918997.1pijWu&_u=h82e7qs2ebe')
    for link in tmall_links:
        assert get_origin_source_by_url(link) == 'taobao.com'

    # 95095
    help_me_links = ('https://detail.yao.95095.com/item.htm?spm=a230r.1.14.22.USvP4s&id=523168907868&ns=1&abbucket=5',)
    for link in help_me_links:
        assert get_origin_source_by_url(link) == 'taobao.com'

    kaola_links = ('http://www.kaola.com/product/29310.html?referId=brand&from=page1&position=15&istext=0',)
    for link in kaola_links:
        assert get_origin_source_by_url(link) == 'www.kaola.com'

    booking_links = ('http://www.booking.com/hotel/lk/the-safari.zh-cn.html',)
    for link in booking_links:
        assert get_origin_source_by_url(link) == 'www.booking.com'

    sixpm_links = ('http://www.6pm.com/pink-pepper-pistol-natural',)
    for link in sixpm_links:
        assert get_origin_source_by_url(link) == 'www.6pm.com'

    whatever_links = ('http://www.baidu.com',
                       'http://www.weibo.com',
                       'http://www.!$#@!$#@!.me',
                       'http://www.ele.me',
                       'http://www.douban_stupid.com')
    for link in whatever_links:
        assert get_origin_source_by_url(link) is None

    amazon_links = ('http://www.amazon.cn/gp/product/B00OXPX2JO/ref=gb1h_img_c-2_9092_4605d068?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=17ET58WYCQRB3AWYH50K&pf_rd_i=20&pf_rd_p=249079092',
                    'http://www.amazon.cn/gp/product/B00V4D3SQA/ref=gb1h_img_c-2_9092_c9adcdf0?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=1RGPWPZWSXY13YG6MN10&pf_rd_i=20&pf_rd_p=249079092')
    for link in amazon_links:
        assert get_origin_source_by_url(link) == 'amazon.com'
