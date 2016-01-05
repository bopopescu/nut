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
        'amazon_com': amazon_com_links(),
    }


@pytest.fixture
def taobao_links(): 
    return {
    'https://item.taobao.com/item.htm?spm=a21bo.7724922.8446.2.oi90zh&scm=1007.10325.17076.0&id=43352358270': '43352358270',
    'https://item.taobao.com/item.htm?spm=5704.2075955.1998837601.98.GHug7u&id=522087255299': '522087255299',
    'https://item.taobao.com/item.htm?spm=a219e.7778345.24768.9.oIZ6TF&id=37353406383': '37353406383',
    'https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.3.jdEeMZ&id=524659592741': '524659592741',
    'https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.132.2Wnn8I&id=524447761628': '524447761628',
    'https://item.taobao.com/item.htm?spm=a1z09.2.0.0.NMMzy2&id=45074255719&_u=r82e7qs23aa': '45074255719',
    'https://item.taobao.com/item.htm?spm=a1z0k.7386009.1997989141.25.ZHDCRp&id=525579185481&_u=&pvid=&scm=': '525579185481',
    'https://item.taobao.com/item.htm?spm=a1z0k.7385961.1997985097.d4918997.V7o5pD&id=22070372914&_u=s82e7qsa0b9': '22070372914',
    }


@pytest.fixture
def tmall_links(): 
    return {
    'https://detail.tmall.com/item.htm?spm=608.7065813.ne.1.Qy6vnN&id=522022069242&tracelog=jubuybigpic': '522022069242',
    'https://detail.tmall.com/item.htm?id=525566206070&spm=a1z0k.7386009.1997989141.7.ZHDCRp': '525566206070',
    'https://detail.tmall.com/item.htm?spm=a1z10.5-b.w4011-6947701451.28.gkW48M&id=524854465546&rn=28e1186d09057bfe346db810d1baafbe&abbucket=17': '524854465546',
    'https://detail.tmall.com/item.htm?spm=a230r.1.14.51.hQrvPf&id=21361619524&ns=1&_u=hfgvk8386d7&abbucket=8': '21361619524',
    'https://detail.tmall.com/item.htm?spm=a1z10.1-b.w5003-13095458026.26.bs1ggb&id=520847275617&scene=taobao_shop': '520847275617',
    'https://detail.tmall.com/item.htm?spm=a220o.1000855.1998025129.1.FSm5pB&id=524201323414&pvid=a84033e0-237f-4095-9d0e-70376408af82&abbucket=_AB-M32_B10&acm=03054.1003.1.609376&aldid=oMPo8uD5&abtest=_AB-LR32-PV32_2410&scm=1007.12559.18851.100200300000000&pos=1': '524201323414',
    }


@pytest.fixture
def jd_links(): 
    return {
        'http://item.jd.com/880516.html': '880516',
        'http://item.jd.com/234579.html': '234579',
        'http://item.jd.com/1090086.html': '1090086',
        'http://item.jd.com/11791659.html': '11791659',
    }


@pytest.fixture
def amazon_cn_links(): 
    return {
        'http://www.amazon.cn/gp/product/B00V4D3SQA/ref=gb1h_img_c-2_9092_c9adcdf0?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=1RGPWPZWSXY13YG6MN10&pf_rd_i=20&pf_rd_p=249079092': 'B00V4D3SQA',
        'http://www.amazon.cn/gp/product/B00OXPX2JO/ref=gb1h_img_c-2_9092_4605d068?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=17ET58WYCQRB3AWYH50K&pf_rd_i=20&pf_rd_p=249079092': 'B00OXPX2JO',
        'http://www.amazon.cn/gp/product/B00QJDOLIO/': 'B00QJDOLIO',
        'http://www.amazon.cn/dp/B004AI97MA/ref=gwgfloorv1_AGS_a_1?_encoding=UTF8&ie=UTF8&smid=A2EDK7H33M5FFG&pf_rd_p=257929552&pf_rd_s=desktop-3&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9': 'B004AI97MA',
        'http://www.amazon.cn/dp/B00L50Z50O/ref=gwgfloorv1_SOFTLINE_a_0?pf_rd_p=267223892&pf_rd_s=desktop-5&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9': 'B00L50Z50O',
        'http://www.amazon.cn/dp/B00L9QZU3Q/ref=gwgfloorv1_BMVD_a_2?pf_rd_p=267232112&pf_rd_s=desktop-7&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9': 'B00L9QZU3Q',
    }

@pytest.fixture
def amazon_com_links(): 
    return {
        'http://www.amazon.com/Dr-Martens-Gryphon-Gladiator-Sandals/dp/B00VLVE8GO/ref=pd_sbs_309_6?ie=UTF8&dpID=41vgh4O0Y4L&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=1Z7DKG02QWSYX31XCW9R': 'B00VLVE8GO',
        'http://www.amazon.com/AmazonBasics-Solid-Lightweight-Flannel-Sheet/dp/B00WNJJTK8/ref=sr_1_6?s=bedbath&srs=10112675011&ie=UTF8&qid=1451212622&sr=1-6&refinements=p_n_material_browse%3A316557011': 'B00WNJJTK8',
        'http://www.amazon.com/gp/product/B015E8U6EM/ref=br_asw_pdt-12?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-5&pf_rd_r=1H0S4FRE8TYGWY1JNK15&pf_rd_t=36701&pf_rd_p=2311356602&pf_rd_i=desktop': 'B015E8U6EM',
        'http://www.amazon.com/gp/product/B002LHIQKQ/ref=s9_cartx_gw_d99_g194_i1?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-3&pf_rd_r=1H0S4FRE8TYGWY1JNK15&pf_rd_t=36701&pf_rd_p=2084660942&pf_rd_i=desktop': 'B002LHIQKQ',
        'http://www.amazon.com/Adobe-65263875-Photoshop-Elements-14/dp/B014GP8XGM/ref=lp_909664_1_1?s=software&ie=UTF8&qid=1451212649&sr=1-1': 'B014GP8XGM',
        'http://www.amazon.com/Adobe-65237578-Photoshop-Lightroom-6/dp/B00VWCKJVA/ref=pd_sim_65_4?ie=UTF8&dpID=51IBwdZ4aQL&dpSrc=sims&preST=_AC_UL160_SR119%2C160_&refRID=0ZAJEB4GE1GRF3Q7SD8D': 'B00VWCKJVA'
    }


@pytest.fixture
def help_me_links(): 
    return {
        'https://detail.yao.95095.com/item.htm?spm=a230r.1.14.22.USvP4s&id=523168907868&ns=1&abbucket=5': '523168907868',
    }


@pytest.fixture
def kaola_links(): 
    return {
        'http://www.kaola.com/product/29310.html?referId=brand&from=page1&position=15&istext=0': '29310',
        'http://www.kaola.com/product/11250.html?referId=brand&from=page1&position=0&istext=0':'11250',
        'http://www.kaola.com/product/15529.html?referId=brand&from=page1&position=4&istext=0':'15529',
        'http://www.kaola.com/product/10065.html?from=%E6%AF%8D%E5%A9%B4%E4%B8%93%E5%8C%BA&block=3&location=1&position=6':'10065',
        'http://www.kaola.com/product/22743.html?from=%E6%9C%8D%E9%A5%B0%E9%9E%8B%E5%8C%85&block=3&location=6&position=11':'22743'
    }


@pytest.fixture
def booking_links(): 
    return {
        'http://www.booking.com/hotel/lk/the-safari.zh-cn.html': '',
    }


@pytest.fixture
def six_pm_links(): 
    return {
        'http://www.6pm.com/pink-pepper-pistol-natural': '',
    }
