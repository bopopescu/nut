#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def links():
    return {
        'taobao': taobao_links(),
        'tmall': tmall_links(),
        'jd': jd_links(),
        '95095': help_me_links(),
        'kaola': kaola_links(),
        'booking': booking_links(),
        '6pm': six_pm_links(),
        'amazon_cn': amazon_cn_links(),
        'amazon_au': amazon_au_links(),
        'amazon_br': amazon_br_links(),
        'amazon_de': amazon_de_links()
    }


@pytest.fixture
def taobao_links():
    return {
        'https://item.taobao.com/item.htm?spm=a21bo.7724922.8446.2.oi90zh&scm=1007.10325.17076.0&id=43352358270':'43352358270',
        'https://item.taobao.com/item.htm?spm=5704.2075955.1998837601.98.GHug7u&id=522087255299':'522087255299',
        'https://item.taobao.com/item.htm?spm=a219e.7778345.24768.9.oIZ6TF&id=37353406383':'37353406383',
    }


@pytest.fixture
def tmall_links():
    return {
        'https://detail.tmall.com/item.htm?spm=a1z10.5-b.w4011-6947701451.28.gkW48M&id=524854465546&rn=28e1186d09057bfe346db810d1baafbe&abbucket=17':'524854465546',
        'https://detail.tmall.com/item.htm?spm=a230r.1.14.51.hQrvPf&id=21361619524&ns=1&_u=hfgvk8386d7&abbucket=8':'21361619524',
        'https://detail.tmall.com/item.htm?id=524204082213&spm=a1z0k.7385961.1997985097.d4918997.1pijWu&_u=h82e7qs2ebe':'524204082213',
    }


@pytest.fixture
def jd_links():
    return {
        'http://item.jd.com/880516.html':'880516',
        'http://item.jd.com/234579.html':'234579',
        'http://item.jd.com/1090086.html':'1090086',
    }



@pytest.fixture
def amazon_cn_links():
    return {
        'http://www.amazon.cn/gp/product/B00V4D3SQA/ref=gb1h_img_c-2_9092_c9adcdf0?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=1RGPWPZWSXY13YG6MN10&pf_rd_i=20&pf_rd_p=249079092':'B00V4D3SQA',
        'http://www.amazon.cn/gp/product/B00OXPX2JO/ref=gb1h_img_c-2_9092_4605d068?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=17ET58WYCQRB3AWYH50K&pf_rd_i=20&pf_rd_p=249079092':'B00OXPX2JO',
    }


@pytest.fixture
def amazon_au_links():
    return {
        'http://www.amazon.com.au/Sweet-Soul-Home-Book-ebook/dp/B019E5Y1H4/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1450428845&sr=1-1':'B019E5Y1H4',
    }


@pytest.fixture
def amazon_br_links():
    return {
        'http://www.amazon.com.br/gp/product/B018JKRPVY/ref=s9_ri_gw_g351_i3?pf_rd_m=A1ZZFT5FULY4LN&pf_rd_s=desktop-3&pf_rd_r=0GJPRYHYP96Y9WQCZMKE&pf_rd_t=36701&pf_rd_p=2055627422&pf_rd_i=desktop':'B018JKRPVY',
    }


@pytest.fixture
def amazon_de_links():
    return {
        'http://www.amazon.de/gp/product/B00GS0UFMO/ref=s9_simh_gw_p309_d15_i1?pf_rd_m=A3JWKAKR8XB7XF&pf_rd_s=desktop-1&pf_rd_r=0EQSZ3T94Z4S0HPJJS1K&pf_rd_t=36701&pf_rd_p=585296347&pf_rd_i=desktop':'B00GS0UFMO',
    }

@pytest.fixture
def help_me_links():
    return {
        'https://detail.yao.95095.com/item.htm?spm=a230r.1.14.22.USvP4s&id=523168907868&ns=1&abbucket=5':'523168907868',
    }


@pytest.fixture
def kaola_links():
    return {
        'http://www.kaola.com/product/29310.html?referId=brand&from=page1&position=15&istext=0':'29310'
    }


@pytest.fixture
def booking_links():
    return {
        'http://www.booking.com/hotel/lk/the-safari.zh-cn.html':'',
    }


@pytest.fixture
def six_pm_links():
    return {
        'http://www.6pm.com/pink-pepper-pistol-natural':'',
    }
