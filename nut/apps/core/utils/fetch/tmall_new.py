# -*- coding: utf-8 -*-

import requests
import re
from time import time
from bs4 import BeautifulSoup
from urllib import unquote
from hashlib import md5


import json


from django.utils.log import getLogger
log = getLogger('django')


IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"

origin_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Referer': 'http://detail.tmall.com/item.htm?id=44691754172'
    }


class Tmall():
    def __init__(self, item_id):
        self.item_id = item_id
        self.html = self.fetch_html()
        self.soup = BeautifulSoup(self.html, from_encoding="gb18030")


    @property
    def headers(self):
        return self._headers

    @property
    def nick(self):
        self._nick = self._headers.get('at_nick')
        if not self._nick:
            return ""
        return unquote(self._nick)

    @property
    def cid(self):
        cat = self.headers.get('X-Category')
        try:
            _cid = cat.split('/')
            return _cid[-1]
        except AttributeError, e:
            log.error("Error: %s", e.message)
        return 0

    @property
    def desc(self):
        return self.soup.title.string[0:-12]

    @property
    def price(self):
        return self._price

    @property
    def brand(self):
        seller_soup = self.soup.select("ul.attributes-list li")
        if not seller_soup:
            seller_soup = self.soup.select("ul#J_AttrUL li")
        if seller_soup > 0:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()
        return ''

    @property
    def images(self):
        _images = list()
        fimg = self.soup.select("#J_ImgBooth")

        fjpg = fimg[0].attrs.get('data-src')
        if not fjpg:
            fjpg = fimg[0].attrs.get('src')

        fjpg = re.sub(IMG_POSTFIX, "", fjpg)

        if "http" not in fjpg:
            fjpg = "http:" + fjpg

        _images.append(fjpg)

        optimgs = self.soup.select("ul#J_UlThumb li a img")

        for op in optimgs:
            try:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError, e:
                optimg = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if optimg in _images:
                continue
            _images.append(optimg)
        return _images

    @property
    def shoplink(self):
        shopidtag = re.findall('shopId:"(\d+)', self.html)

        if len(shopidtag) > 0:
            shoplink = "http://shop"+shopidtag[0]+".taobao.com"
            return shoplink
        return "http://chaoshi.tmall.com/"

    def fetch_html(self):
        start_url = self.get_start_url(self.item_id)
        html = ""
        with requests.Session() as s :
                r = s.get(start_url, verify=False, headers=self.get_tmall_header(), cookies=self.get_tmall_cookie())
                html = r.text
                self._headers = r.headers
        #       price must be retrieved as soon as possible
                script_url =  self.fix_script_url(self.extract_price_script_url(html))
                price_script_response  = s.get(script_url, headers=self.get_tmall_header()).text
                self._price = self.process_price_response(price_script_response)
        return html

    def process_price_response(self,price_script_response):
        reg = re.compile('\((.*)\)')
        m = reg.search(price_script_response)
        price_json = json.loads(m.group(1))
        price = self.get_price_by_price_json(price_json)

        return price

    def get_price_by_price_json(self, entity_info):
        price = 0
        prices = []
        if entity_info['isSuccess']:
            try:
                priceInfo =  entity_info['defaultModel']['itemPriceResultDO']['priceInfo']
                for k,v in priceInfo.iteritems():
                    prices.append(priceInfo[k]['price'])
                    # may be there is multiple promotionList ... TODO
                    if priceInfo[k]['promotionList'] and len(priceInfo[k]['promotionList']):
                         for promo in priceInfo[k]['promotionList']:
                             try :
                                 prices.append(promo['price'])
                                 prices.append(promo['extraPromPrice'])
                             except KeyError:
                                 continue
            except Exception as e:
                # TODO: log error
                pass
                # print e.message
                # log.error(e.message)
            finally:
                if len(prices) > 0 :
                    price = min(map(float,prices))
                else:
                    price = 0
        else:
            price = 0
        return price

    def extract_price_script_url(self,html_str):
        reg = re.compile('url=\'(\S*)\'')
        m = reg.search(html_str)
        return m.group(1)

    def fix_script_url(self,script_url):
        script_url = script_url.replace('mdskip.taobao.com', 'mdskip.tmall.com')
        l = list()
        prepend = ''
        if not 'http:' in script_url:
            prepend = 'http:'
        l.append("callback=setMdskip")
        l.append("timestamp=%d"%int(time()))
        return  "%s%s&%s"%(prepend,script_url,'&'.join(l))

    def get_tmall_header(self):
        tmall_header = {
            'Cookie':'cna=C6IRC8X/ODgCAd6BFDvWbabx; swfstore=293511; whl=-1%260%260%260; CNZZDATA1000279581=2084491831-1431329588-http%253A%252F%252Fsubject.tmall.com%252F%7C1432794651; lzstat_uv=11965390701316469673|2934243@2674749@3576861; lzstat_ss=140379413_3_1398070003_2934243|815277699_0_1422723118_2674749|2999861223_2_1434841102_3576861; ucn=center; tkmb=e=zGU0g6e1d7xnyW5i7tVTF34AiQ6j29rfKzBnvRc7iWAKnIJfZf8qogh3jq5OecGVnIZVGJ6iJNJUooZBX7Ci3Kb86eKaBMLWSFMJq3gfdbiOtqM14m8TUixr3LK%2FQUevmmOcDn3qcCAD0AiwnIeHDgP50F2QwFA5ztriqzRqqT9%2Fh3aZffAL0k6U0Q%3D%3D&iv=0&et=1436260677; ck1=; _tb_token_=e3eab0131bee0; uc3=nk2=F5fFAGakplCe&id2=UU21bCqQ9jo%3D&vt3=F8dASM2ebvybuPH%2FldI%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=tayaktaka; tracknick=tayaktaka; cookie2=2c4c3d08862516f8b17f01d55c31d074; skt=7b0c61cad5da6b2f; t=5070ce985c3f11b15a524d6788515bf0; tk_trace=1; pnm_cku822=172UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktyTnpCdkJ%2BRXxIfSs%3D%7CU2xMHDJ7G2AHYg8hAS8WKQcnCU4nTGI0Yg%3D%3D%7CVGhXd1llXGVZbVVhVWlSa19qXWBCe05zR3xDf0p%2BS3JKcEl0QW85%7CVWldfS0TMw8wDzAQLg4gdlNlSx1L%7CVmhIGCEdPRwgFCsUNAgxDDAQLhsvFjYKPgE8HCAdKBU1CT0CPx8jHiYcShw%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; cq=ccp%3D1; l=AgkJbJ5afOfrqhFMGy4g0hBRmTtjVv2I; isg=E67B4BE00CF880E3F80FAD48EBEE149E',
            'User-Agent':'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
         }
        tmall_header.update(origin_headers)
        return tmall_header

    def get_start_url(self, id):
        return "http://detail.tmall.com/item.htm?id=%s"%id

    def get_tmall_cookie(self):
        return {}

    def res(self):
        result = {
            "desc": self.desc,
			"cid": self.cid,
			"promprice" : self.price,
            "price": self.price,
			# "category" : "",
			"imgs": self.images,
			"count": 0,
			"reviews": 0,
			"nick": self.nick,
			"shop_link": self.shoplink,
			"location": "",
            "brand": self.brand
        }
        return result



def tmall_test_fn():
    product = Tmall('3362046923')
    print product.res()
    pass

if __name__=="__main__":
    tmall_test_fn()