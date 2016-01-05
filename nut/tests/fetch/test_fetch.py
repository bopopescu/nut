#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import pytest

from time import sleep

from apps.fetch import Amazon
from apps.fetch import JD
from apps.fetch import TaoBao
from apps.fetch import Tmall


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'fetch/data')


def clean_image_id(image_url):
    return image_url.split('/')[-1]


@pytest.mark.parametrize('provider,key', (
        (TaoBao, 'taobao'),
        (Tmall, 'tmall'),
        (Amazon, 'amazon_cn'),
        # (Amazon, 'amazon_com'),
        (JD, 'jd'),
        # (Kaola, 'kaola'),
        # (Booking, 'booking'),
        # (SixPM, '6pm'),
        (TaoBao, '95095'),
))
def test_cache_all_html_files(provider, key, links):
    for link in links[key].keys():
        provider_instance = provider(link)
        file_path = '%s/%s_%s.html' % (data_dir, key, provider_instance.origin_id)
        if not os.path.isfile(file_path):
            html_file = codecs.open(file_path, 'w', 'utf-16')
            provider_instance.fetch()
            html_file.write(provider_instance.html_source.decode('utf8'))
            html_file.close()
            sleep(5)


@pytest.mark.parametrize('url,origin_id,cid,title,price,brand,link,images', (
    ('http://www.amazon.cn/gp/product/B00V4D3SQA/ref=gb1h_img_c-2_9092_c9adcdf0?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=1RGPWPZWSXY13YG6MN10&pf_rd_i=20&pf_rd_p=249079092',
     'B00V4D3SQA', ('92450071',), u'KNIRPS 克尼普斯 防风防晒五折手开伞小巧89 811 100黑色红点大奖',
     567.00, u'KNIRPS 克尼普斯', 'http://amazon.cn/dp/B00V4D3SQA', [u'http://ec4.images-amazon.com/images/I/31bioU0uBAL.jpg', u'http://ec4.images-amazon.com/images/I/41tgKrtHErL.jpg', u'http://ec4.images-amazon.com/images/I/41BpaIog5GL.jpg', u'http://ec4.images-amazon.com/images/I/51c028MvFbL.jpg', u'http://ec4.images-amazon.com/images/I/41q%2BUDo2nBL.jpg', u'http://ec4.images-amazon.com/images/I/51-oVebl8vL.jpg']),
    ('http://www.amazon.cn/gp/product/B00OXPX2JO/ref=gb1h_img_c-2_9092_4605d068?pf_rd_m=A1AJ19PSB66TGU&pf_rd_t=701&pf_rd_s=center-new-2&pf_rd_r=17ET58WYCQRB3AWYH50K&pf_rd_i=20&pf_rd_p=249079092',
     'B00OXPX2JO', ('2180869051', ), u'delonghi 德龙 火龙4系列10片电子控温电热油汀/电暖气 TRD41020T',
     1650.00, u'De’Longhi 德龙','http://amazon.cn/dp/B00OXPX2JO', [u'http://ec4.images-amazon.com/images/I/71PyuqeQ2EL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/71d0cWRV1HL._SL1500_.jpg']),
    ('http://www.amazon.cn/gp/product/B00QJDOLIO/',
     'B00QJDOLIO', ('116087071', ), u'全新Kindle Paperwhite电子书阅读器：300 ppi电子墨水触控屏、内置阅读灯、超长续航',
     958.00, u'Amazon', 'http://amazon.cn/dp/B00QJDOLIO', [u'http://ec4.images-amazon.com/images/I/71eFIzxtaSL._SL1000_.jpg', u'http://ec4.images-amazon.com/images/I/61pdIJDfhCL._SL1000_.jpg', u'http://ec4.images-amazon.com/images/I/71c3mpvFrVL._SL1000_.jpg', u'http://ec4.images-amazon.com/images/I/71wrqV8umiL._SL1000_.jpg', u'http://ec4.images-amazon.com/images/I/61FEwLhxglL._SL1000_.jpg', u'http://ec4.images-amazon.com/images/I/41kxkn1qtsL._SL1000_.jpg']),
    ('http://www.amazon.cn/dp/B004AI97MA/ref=gwgfloorv1_AGS_a_1?_encoding=UTF8&ie=UTF8&smid=A2EDK7H33M5FFG&pf_rd_p=257929552&pf_rd_s=desktop-3&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9',
     'B004AI97MA', ('422481071',), u'Bio-Oil Purcellin油，4.2盎司（119g）',
     103.44, u'Bio-Oil', 'http://amazon.cn/dp/B004AI97MA', [u'http://ec4.images-amazon.com/images/I/71MB0CW7eBL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/41FIFcKinzL.jpg', u'http://ec4.images-amazon.com/images/I/71OUli2RkjL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/71HYGSfpcuL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/813ivKf5kSL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/31icoPpBYJL.jpg', u'http://ec4.images-amazon.com/images/I/81rl23UAshL._SL1246_.jpg', u'http://ec4.images-amazon.com/images/I/81Q-qY0R-uL._SL1500_.jpg', u'http://ec4.images-amazon.com/images/I/71-qmWcBaIL._SL1500_.jpg']),
    ('http://www.amazon.cn/dp/B00L50Z50O/ref=gwgfloorv1_SOFTLINE_a_0?pf_rd_p=267223892&pf_rd_s=desktop-5&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9',
     'B00L50Z50O', ('2154361051',), u'MANGO 女式 条纹质感毛衣 BOA3 33023559',
     359.00, u'MANGO', 'http://amazon.cn/dp/B00L50Z50O', [u'http://ec4.images-amazon.com/images/I/41yRJYCNTXL.jpg', u'http://ec4.images-amazon.com/images/I/61RW-xJ9FLL._UL1500_.jpg', u'http://ec4.images-amazon.com/images/I/717iAIJZeIL._UL1500_.jpg', u'http://ec4.images-amazon.com/images/I/61NdMEh2JML._UL1500_.jpg']),
    ('http://www.amazon.cn/dp/B00L9QZU3Q/ref=gwgfloorv1_BMVD_a_2?pf_rd_p=267232112&pf_rd_s=desktop-7&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=14NSY8HXJ9EGMS0DAAF9',
     'B00L9QZU3Q', ('658738051', '660523051', '660522051'), u'爆炸头米拉(典藏版)(套装共3册)(最温暖人心的儿童成长绘本)',
     30.20, None, 'http://amazon.cn/dp/B00L9QZU3Q', [u'http://ec4.images-amazon.com/images/I/81jClYqcJ9L.jpg', u'http://ec4.images-amazon.com/images/I/81Ok3v4VxiL.jpg'])
))
def test_amazon_cn_fetch(url, origin_id, cid, title, price, brand, link, images):
    provider = Amazon(link)
    source_file = open('%s/amazon_cn_%s.html' % (data_dir, provider.origin_id), 'r')
    html_source = source_file.read()
    provider.html_source = html_source
    source_file.close()
    assert provider.origin_id == origin_id
    assert provider.price == price
    assert provider.brand == brand
    assert provider.foreign_price == 0.0
    assert provider.title == title
    assert provider.link == link
    assert provider.cid in cid
    provider_images_id = [clean_image_id(image) for image in provider.images]
    images_id = [clean_image_id(image) for image in images]
    assert set(provider_images_id) >= set(images_id)

#
# @pytest.mark.parametrize('link,origin_id,foreign_price,brand,url', (
#     ('http://www.amazon.com/Dr-Martens-Gryphon-Gladiator-Sandals/dp/B00VLVE8GO/ref=pd_sbs_309_6?ie=UTF8&dpID=41vgh4O0Y4L&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=1Z7DKG02QWSYX31XCW9R',
#      'B00VLVE8GO', 108.00, u'Dr. Martens', 'http://www.amazon.com/dp/B00VLVE8GO'),
#     ('http://www.amazon.com/AmazonBasics-Solid-Lightweight-Flannel-Sheet/dp/B00WNJJTK8/ref=sr_1_6?s=bedbath&srs=10112675011&ie=UTF8&qid=1451212622&sr=1-6&refinements=p_n_material_browse%3A316557011',
#      'B00WNJJTK8', 44.99, u'AmazonBasics', 'http://www.amazon.com/dp/B00WNJJTK8'),
#     ('http://www.amazon.com/gp/product/B015E8U6EM/ref=br_asw_pdt-12?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-5&pf_rd_r=1H0S4FRE8TYGWY1JNK15&pf_rd_t=36701&pf_rd_p=2311356602&pf_rd_i=desktop',
#      'B015E8U6EM', 824.10, u'Apple', 'http://www.amazon.com/dp/B015E8U6EM'),
#     ('http://www.amazon.com/gp/product/B002LHIQKQ/ref=s9_cartx_gw_d99_g194_i1?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-3&pf_rd_r=1H0S4FRE8TYGWY1JNK15&pf_rd_t=36701&pf_rd_p=2084660942&pf_rd_i=desktop',
#      'B002LHIQKQ', 29.99, u'Fresh', 'http://www.amazon.com/dp/B002LHIQKQ'),
#     ('http://www.amazon.com/Adobe-65263875-Photoshop-Elements-14/dp/B014GP8XGM/ref=lp_909664_1_1?s=software&ie=UTF8&qid=1451212649&sr=1-1',
#      'B014GP8XGM', 69.99, u'Adobe', 'http://www.amazon.com/dp/B014GP8XGM'),
#     ('http://www.amazon.com/Adobe-65237578-Photoshop-Lightroom-6/dp/B00VWCKJVA/ref=pd_sim_65_4?ie=UTF8&dpID=51IBwdZ4aQL&dpSrc=sims&preST=_AC_UL160_SR119%2C160_&refRID=0ZAJEB4GE1GRF3Q7SD8D',
#      'B00VWCKJVA', 175.99, u'Adobe', 'http://www.amazon.com/dp/B00VWCKJVA')
# ))
# def test_amazon_com_fetch(link, origin_id, foreign_price, brand, url):
#     provider = Amazon(link)
#     source_file = open('%s/amazon_com_%s.html' % (data_dir, provider.origin_id), 'r')
#     html_source = source_file.read()
#     provider.html_source = html_source
#     source_file.close()
#     assert provider.origin_id == origin_id
#     assert provider.price < foreign_price
#     assert provider.price is not 0.00
#     assert provider.price is True
#     assert provider.brand == brand
#     assert provider.link == url
#
#
@pytest.mark.parametrize('url,origin_id,title,shop_nick,shop_link,cid,images,price,brand,link', (
    ('https://item.taobao.com/item.htm?spm=5704.2075955.1998837601.98.GHug7u&id=522087255299',
     '522087255299', u'北欧宜家简约家具真皮床 双人床婚床真皮床卧室家具软床极美家具',
     u'欧舒涵', u'oushuhan.taobao.com', u'50020000', ['https://gd4.alicdn.com/bao/uploaded/i4/TB1mpkIKVXXXXXLapXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd2.alicdn.com/imgextra/i2/2557649867/TB27qGFfpXXXXbYXpXXXXXXXXXX_!!2557649867.jpg', 'https://gd1.alicdn.com/imgextra/i1/2557649867/TB2axuYfpXXXXXOXXXXXXXXXXXX_!!2557649867.jpg', 'https://gd4.alicdn.com/imgextra/i4/2557649867/TB2sWW8fpXXXXXjXXXXXXXXXXXX_!!2557649867.jpg', 'https://gd3.alicdn.com/imgextra/i3/2557649867/TB2RLaNfpXXXXawXpXXXXXXXXXX_!!2557649867.jpg'],
     2380.00, u'欧舒涵', 'http://item.taobao.com/item.htm?id=522087255299'),
    ('https://item.taobao.com/item.htm?spm=a21bo.7724922.8446.2.oi90zh&scm=1007.10325.17076.0&id=43352358270',
     '43352358270', u'CHICMILD春韩版时尚优雅复古八角帽 显肤红色画家帽甜美贝雷帽女',
     u'美堂娜娜', u'heyduck.taobao.com', u'302910', ['https://gd1.alicdn.com/bao/uploaded/i1/TB1b6NPHXXXXXb2XXXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd2.alicdn.com/imgextra/i2/24756913/TB2T.hRbFXXXXbrXXXXXXXXXXXX_!!24756913.jpg', 'https://gd4.alicdn.com/imgextra/i4/24756913/TB2XzNNbFXXXXXDXpXXXXXXXXXX_!!24756913.jpg', 'https://gd4.alicdn.com/imgextra/i4/24756913/TB2aIdVbFXXXXasXXXXXXXXXXXX_!!24756913.jpg'],
     39.00, u'CHICMILD', 'http://item.taobao.com/item.htm?id=43352358270'),
    ('https://item.taobao.com/item.htm?spm=a219e.7778345.24768.9.oIZ6TF&id=37353406383',
     '37353406383', u'百凤野鸡蛋30枚装 农家散养 柴鸡蛋 草鸡蛋 新鲜七彩野山鸡土鸡蛋',
     u'miya9486', u'baifengzhenqin.taobao.com', u'50012385', ['https://gd1.alicdn.com/imgextra/i1/574988632/TB2kyXEcFXXXXXgXXXXXXXXXXXX_!!574988632.jpg', 'https://gd2.alicdn.com/imgextra/i2/574988632/TB2lTtscFXXXXb8XpXXXXXXXXXX_!!574988632.jpg', 'https://gd1.alicdn.com/imgextra/i1/574988632/TB2kyXEcFXXXXXgXXXXXXXXXXXX_!!574988632.jpg', 'https://gd4.alicdn.com/imgextra/i4/574988632/TB2A6rmdpXXXXagXpXXXXXXXXXX_!!574988632.jpg'],
     86.90, u'百凤珍禽', 'http://item.taobao.com/item.htm?id=37353406383'),
    ('https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.3.jdEeMZ&id=524659592741',
     '524659592741', u'shutupbaby2015 新款女装 剪裁毛边做旧高腰牛仔裤', u'zhaiq68',
     u'shutupbaby.taobao.com', u'162205', ['https://gd1.alicdn.com/bao/uploaded/i1/TB15_jNKFXXXXbqXpXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd1.alicdn.com/imgextra/i1/32920404/TB2ilrShFXXXXXSXXXXXXXXXXXX_!!32920404.jpg'],
     499.00, u'shut up baby', 'http://item.taobao.com/item.htm?id=524659592741'),
    ('https://item.taobao.com/item.htm?spm=a1z0d.6639537.1997196601.132.2Wnn8I&id=524447761628',
     '524447761628', u'Nars 经典必备双色眼影 portobello 大地色系 打底 亚光',
     u'huryguo', u'shop34119813.taobao.com', u'50010796', ['https://gd1.alicdn.com/bao/uploaded/i1/TB1vulSKFXXXXazXFXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd4.alicdn.com/imgextra/i4/52245477/TB22snshpXXXXcwXpXXXXXXXXXX_!!52245477.jpg', 'https://gd1.alicdn.com/imgextra/i1/52245477/TB2H3LJhpXXXXXeXpXXXXXXXXXX_!!52245477.jpg', 'https://gd3.alicdn.com/imgextra/i3/52245477/TB29XTUhpXXXXbaXXXXXXXXXXXX_!!52245477.jpg', 'https://gd2.alicdn.com/imgextra/i2/52245477/TB2926OhpXXXXcfXXXXXXXXXXXX_!!52245477.jpg'],
     178.00, u'NARS', 'http://item.taobao.com/item.htm?id=524447761628'),
    ('https://item.taobao.com/item.htm?spm=a1z09.2.0.0.NMMzy2&id=45074255719&_u=r82e7qs23aa',
     '45074255719', u'香港代购NARS丝绒唇笔/唇膏笔damned/dolce vita/DRAGON GIRL/DV',
     u'daisy08018', u'shop120687085.taobao.com', u'50010801', ['https://gd4.alicdn.com/bao/uploaded/i4/TB13OcHIpXXXXa5XXXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd3.alicdn.com/imgextra/i3/2491887383/TB25uxjdFXXXXXTXXXXXXXXXXXX_!!2491887383.jpg', 'https://gd1.alicdn.com/imgextra/i1/2491887383/TB2ZSEQdpXXXXXfXFXXXXXXXXXX_!!2491887383.jpg', 'https://gd4.alicdn.com/imgextra/i4/TB1mQPNHFXXXXamXFXXXXXXXXXX_!!0-item_pic.jpg'],
     60, u'NARS', 'http://item.taobao.com/item.htm?id=45074255719'),
    ('https://item.taobao.com/item.htm?spm=a1z0k.7386009.1997989141.25.ZHDCRp&id=525579185481&_u=&pvid=&scm=',
     '525579185481', u'待上架 米马杂货 公道杯',
     u'米马', u'mimahome.taobao.com', u'121398024', ['https://gd4.alicdn.com/bao/uploaded/i4/TB1ARp1LXXXXXbtaXXXXXXXXXXX_!!0-item_pic.jpg', 'https://gd3.alicdn.com/imgextra/i3/90149/TB2Lj8miVXXXXXnXXXXXXXXXXXX_!!90149.jpg', 'https://gd4.alicdn.com/imgextra/i4/90149/TB2VCIQiFXXXXbVXpXXXXXXXXXX_!!90149.jpg', 'https://gd3.alicdn.com/imgextra/i3/90149/TB2nBAUiFXXXXa7XpXXXXXXXXXX_!!90149.jpg', 'https://gd2.alicdn.com/imgextra/i2/90149/TB2bKNiiVXXXXX.XXXXXXXXXXXX_!!90149.jpg'],
     121.60, None, 'http://item.taobao.com/item.htm?id=525579185481'),
    ('https://item.taobao.com/item.htm?spm=a1z0k.7385961.1997985097.d4918997.V7o5pD&id=22070372914&_u=s82e7qsa0b9',
     '22070372914', u'[现货包邮]日本代购Tabio靴下屋假大腿袜性感拼接长筒连裤袜丝袜',
     u'pinglucky777', u'sanpufanghui.taobao.com', u'50006846', ['https://gd3.alicdn.com/bao/uploaded/i3/17391030570728225/T1k1ZUXdFcXXXXXXXX_!!0-item_pic.jpg', 'https://gd3.alicdn.com/imgextra/i3/17391019243689044/T1u8gjXoBcXXXXXXXX_!!0-item_pic.jpg', 'https://gd1.alicdn.com/imgextra/i1/1085107391/T2aMnhXntaXXXXXXXX_!!1085107391.jpg', 'https://gd4.alicdn.com/imgextra/i4/1085107391/T218rhXbBaXXXXXXXX_!!1085107391.jpg', 'https://gd4.alicdn.com/imgextra/i4/1085107391/T22kiYXbNbXXXXXXXX_!!1085107391.jpg'],
     128.00, u'靴下屋', 'http://item.taobao.com/item.htm?id=22070372914')
))
def test_taobao_fetch(url, origin_id, title, shop_nick, shop_link, cid, images,
                      price, brand, link):
    provider = TaoBao(link)
    source_file = open('%s/taobao_%s.html' % (data_dir, provider.origin_id), 'r')
    html_source = source_file.read()
    provider.html_source = html_source
    source_file.close()
    assert provider.origin_id == origin_id
    assert provider.price == price
    assert provider.brand == brand
    assert provider.link == link
    assert provider.shop_nick.upper() == shop_nick.upper()
    assert provider.shop_link == shop_link
    assert provider.title == title
    assert provider.cid == cid
    provider_images_id = [clean_image_id(image) for image in provider.images]
    images_id = [clean_image_id(image) for image in images]
    assert set(provider_images_id) >= set(images_id)


@pytest.mark.parametrize('url,origin_id,title,price,brand,cid,link,images,shop_link,shop_nick', (
    ('https://detail.tmall.com/item.htm?spm=608.7065813.ne.1.Qy6vnN&id=522022069242&tracelog=jubuybigpic',
     '522022069242', u'播 时间煮雨 2016新品 中长款韩版针织七分袖修身显瘦连衣裙', 649.00, u'broadcast/播',
     u'16', 'http://detail.tmall.com/item.htm?id=522022069242', ['https://img.alicdn.com/imgextra/i1/2274693745/TB1VO9hLXXXXXXoXFXXXXXXXXXX_!!0-item_pic.jpg', 'https://img.alicdn.com/imgextra/i1/497244433/TB2sTXMfFXXXXcjXXXXXXXXXXXX_!!497244433.jpg', 'https://img.alicdn.com/imgextra/i3/497244433/TB2QaligpXXXXX9XXXXXXXXXXXX_!!497244433.jpg', 'https://img.alicdn.com/imgextra/i1/497244433/TB2ol.ZgXXXXXaZXpXXXXXXXXXX_!!497244433.jpg', 'https://img.alicdn.com/imgextra/i3/497244433/TB2LCRbgpXXXXbEXXXXXXXXXXXX_!!497244433.jpg'],
     'http://broadcast.tmall.com', u'播官方旗舰店'),
    ('https://detail.tmall.com/item.htm?id=525566206070&spm=a1z0k.7386009.1997989141.7.ZHDCRp',
     '525566206070', u'PullAndBear 女士宽松字母T恤 05239300', 99, u'PULL＆BEAR',
     u'16', 'http://detail.tmall.com/item.htm?id=525566206070', ['https://img.alicdn.com/bao/uploaded/i4/TB1VMt.LXXXXXbHXFXXXXXXXXXX_!!0-item_pic.jpg', 'https://img.alicdn.com/imgextra/i2/1787625780/TB2VzZPiFXXXXb1XpXXXXXXXXXX-1787625780.jpg', 'https://img.alicdn.com/imgextra/i4/1787625780/TB2AE0hiVXXXXagXXXXXXXXXXXX-1787625780.jpg', 'https://img.alicdn.com/imgextra/i2/1787625780/TB2f6NniVXXXXXdXXXXXXXXXXXX-1787625780.jpg', 'https://img.alicdn.com/imgextra/i3/1787625780/TB2o6IRiFXXXXbKXpXXXXXXXXXX-1787625780.jpg'],
     'http://pullandbear.tmall.com', u'pullandbear官方旗舰店'),
    ('https://detail.tmall.com/item.htm?spm=a1z10.5-b.w4011-6947701451.28.gkW48M&id=524854465546&rn=28e1186d09057bfe346db810d1baafbe&abbucket=17',
     '524854465546', u'M＆S/马莎女黑白驯鹿图案长款开衫 T382108', 499, u'M＆S/马莎',
     u'16', 'http://detail.tmall.com/item.htm?id=524854465546', ['https://img.alicdn.com/bao/uploaded/i1/TB1WkRjKVXXXXasXpXXXXXXXXXX_!!0-item_pic.jpg', 'https://img.alicdn.com/imgextra/i4/1061111027/TB2SqLBhVXXXXcPXXXXXXXXXXXX_!!1061111027.jpg', 'https://img.alicdn.com/imgextra/i2/1061111027/TB21ZjhhVXXXXcWXpXXXXXXXXXX_!!1061111027.jpg', 'https://img.alicdn.com/imgextra/i2/1061111027/TB2RQLxhVXXXXXxXpXXXXXXXXXX_!!1061111027.jpg', 'https://img.alicdn.com/imgextra/i2/1061111027/TB2rhfuhVXXXXXOXpXXXXXXXXXX_!!1061111027.jpg'],
     'http://marksandspencer.tmall.com', u'马莎官方旗舰店'),
    ('https://detail.tmall.com/item.htm?spm=a230r.1.14.51.hQrvPf&id=21361619524&ns=1&_u=hfgvk8386d7&abbucket=8',
     '21361619524', u'法国进口 爱乐薇Elle&Vire无盐小杯装黄油10克x6杯 铁塔牌', 13.90, u'Elle＆Vire/爱乐薇',
     u'50016422', 'http://detail.tmall.com/item.htm?id=21361619524', ['https://img.alicdn.com/bao/uploaded/i3/13880025218279011/T1TppFFk4cXXXXXXXX_!!0-item_pic.jpg', 'https://img.alicdn.com/imgextra/i2/383323880/TB2L9nrapXXXXa0XpXXXXXXXXXX_!!383323880.jpg', 'https://img.alicdn.com/imgextra/i4/383323880/TB26V6CapXXXXbwXXXXXXXXXXXX_!!383323880.jpg'],
     'http://xndssp.tmall.com', u'西诺迪斯食品专营店'),
    ('https://detail.tmall.com/item.htm?spm=a220o.1000855.1998025129.1.FSm5pB&id=524201323414&pvid=a84033e0-237f-4095-9d0e-70376408af82&abbucket=_AB-M32_B10&acm=03054.1003.1.609376&aldid=oMPo8uD5&abtest=_AB-LR32-PV32_2410&scm=1007.12559.18851.100200300000000&pos=1',
     '524201323414', u'秋冬折扣 ZARA TRF 女包 亮面拼接手拿包 18879004010', 169.00, u'ZARA',
     u'50006842', 'http://detail.tmall.com/item.htm?id=524201323414', ['https://img.alicdn.com/bao/uploaded/i2/TB1OfTLKpXXXXX_XFXXXXXXXXXX_!!0-item_pic.jpg', 'https://img.alicdn.com/imgextra/i3/2228361831/TB2RsPwhXXXXXcOXXXXXXXXXXXX_!!2228361831.jpg', 'https://img.alicdn.com/imgextra/i3/2228361831/TB2uT2BhXXXXXbnXXXXXXXXXXXX_!!2228361831.jpg', 'https://img.alicdn.com/imgextra/i1/2228361831/TB25ODfhXXXXXbPXpXXXXXXXXXX_!!2228361831.jpg', 'https://img.alicdn.com/imgextra/i2/2228361831/TB2vyrohXXXXXaFXpXXXXXXXXXX_!!2228361831.jpg'],
     'http://zara.tmall.com', u'ZARA官方旗舰店'),
    ('https://detail.tmall.com/item.htm?spm=a1z10.1-b.w5003-13095458026.26.bs1ggb&id=520847275617&scene=taobao_shop',
     '520847275617', u'HollandBarrett HB水解胶原蛋白营养片小分子胶原蛋白180粒/瓶', 127.00, u'Holland＆Barrett',
     u'50026800', 'http://detail.tmall.com/item.htm?id=520847275617', ['https://img.alicdn.com/bao/uploaded/i4/TB1v1yqIFXXXXalapXXXXXXXXXX_!!0-item_pic.jpg','https://img.alicdn.com/imgextra/i1/2274693745/TB2cFEueFXXXXceXpXXXXXXXXXX_!!2274693745.jpg','https://img.alicdn.com/imgextra/i4/2274693745/TB2vBURdVXXXXXaXXXXXXXXXXXX_!!2274693745.jpg','https://img.alicdn.com/imgextra/i4/2274693745/TB29RIEdVXXXXXbXpXXXXXXXXXX_!!2274693745.jpg','https://img.alicdn.com/imgextra/i1/2274693745/TB2jWNvhpXXXXX9XpXXXXXXXXXX-2274693745.jpg'],
     'http://hollandbarrettbjp.tmall.com', u'hollandbarrett旗舰店')
))
def test_tmall_fetch(url, origin_id, title, price, brand, cid, link, images, shop_link, shop_nick):
    provider = Tmall(link)
    source_file = open('%s/tmall_%s.html' % (data_dir, provider.origin_id), 'r')
    html_source = source_file.read()
    provider.html_source = html_source
    source_file.close()
    assert provider.origin_id == origin_id
    assert provider.price == price
    assert provider.brand == brand
    assert provider.link == link
    assert provider.title == title
    assert provider.cid == cid
    assert provider.shop_link == shop_link
    assert provider.shop_nick.upper() == shop_nick.upper()
    provider_images_id = [clean_image_id(image) for image in provider.images]
    images_id = [clean_image_id(image) for image in images]
    assert set(provider_images_id) >= set(images_id)


@pytest.mark.parametrize('url,origin_id', (
    ('http://item.jd.com/880516.html', '880516'),
    ('http://item.jd.com/234579.html', '234579'),
    ('http://item.jd.com/1090086.html', '1090086'),
    ('http://item.jd.com/11791659.html', '11791659'),
))
def test_jd_fetch(url, origin_id):
    provider = JD(url)
    source_file = open('%s/jd_%s.html' % (data_dir, provider.origin_id), 'r')
    html_source = source_file.read()
    provider.html_source = html_source
    source_file.close()
    assert provider.origin_id == origin_id
    assert provider.foreign_price == 0.0
