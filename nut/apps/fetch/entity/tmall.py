# -*- coding: utf-8 -*-
import json
import re
from time import time

import requests

from apps.fetch.entity.base import BaseFetcher
from django.utils.log import getLogger

from apps.fetch.common import clean_price_string


log = getLogger('django')
IMG_POSTFIX = "_\d+x\d+.*\.jpg|_b\.jpg"


class Tmall(BaseFetcher):
    def __init__(self, entity_url, use_phantom=True):
        BaseFetcher.__init__(self, entity_url)
        self.use_phantom = use_phantom
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id()
        self.expected_element = 'div#J_DetailMeta'
        self.timeout = 20

        self.cid_pattern = re.compile(u'"rootCatId":"(?P<cid>\d*)')
        self.price_pattern_a = re.compile(
            u'{"name":"品牌","value":"(?P<brand>[^"]*)"',
            re.MULTILINE | re.UNICODE)
        self.price_pattern_b = re.compile(
            u'brand=(?P<brand>[^&]*)', re.MULTILINE | re.UNICODE)

    @property
    def shop_nick(self):
        nick_tags = ('a.slogo-shopname strong',
                     'li.shopkeeper a',
                     'input[name="seller_nickname"]')
        for nick_tag_name in nick_tags:
            nick_tag = self.soup.select(nick_tag_name)
            if nick_tag:
                return nick_tag[0].text or nick_tag[0].attrs['value']
        return ''

    @property
    def link(self):
        link = 'https://detail.tmall.com/item.htm?id=%s' % self.origin_id
        return link

    def get_origin_id(self):
        params = self.entity_url.split("?")[1]
        for param in params.split("&"):
            tokens = param.split("=")
            if len(tokens) >= 2 and (tokens[0] == "id" or
                                             tokens[0] == "item_id"):
                return tokens[1]

    @property
    def cid(self):
        cid_tag = self.soup.select('input[name="rootCatId"]')
        if cid_tag:
            return cid_tag[0].attrs['value']

        all_scripts = self.soup.select('div#J_DetailMeta script')
        if all_scripts:
            for script in all_scripts:
                cid_tag = self.cid_pattern.findall(script.text)
                if cid_tag:
                    return cid_tag[0]
        return '0'

    @property
    def title(self):
        return self.soup.title.string[0:-12]

    @property
    def price(self):
        price_tag = self.get_price_tag()
        if not price_tag:
            return 0.0
        return price_tag

    def get_price_tag(self):
        price_tag_names = (
            'span.tm-price',
        )
        for price_tag_name in price_tag_names:
            price_tags = self.soup.select(price_tag_name)
            if len(price_tags) > 0:
                prices = []
                for price_tag in price_tags:
                    if price_tag.text:
                        prices.append(clean_price_string(price_tag.text))
                prices.sort()
                return prices[0]

    @property
    def brand(self):
        seller_soup = self.soup.select("ul.attributes-list li")
        if not seller_soup:
            seller_soup = self.soup.select("ul#J_AttrUL li")
        if seller_soup:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()

        seller_soup = self.soup.select("div#J_DetailMeta script")
        if seller_soup:
            for script in seller_soup:
                if script.text:
                    price_tag = self.price_pattern_a.findall(script.text)
                    if price_tag:
                        return price_tag[0]

                    price_tag = self.price_pattern_b.findall(script.text)
                    if price_tag:
                        return price_tag[0]
        return ''

    @property
    def images(self):
        image_list = list()
        img_tags = self.soup.select("#J_ImgBooth")
        if img_tags:
            img_tag = img_tags[0].attrs.get('data-src')
            if not img_tag:
                img_tag = img_tags[0].attrs.get('src')
            img_tag = re.sub(IMG_POSTFIX, "", img_tag)
            if not img_tag.startswith('http') and not img_tag.startswith(
                'https'):
                img_tag = "https:" + img_tag
            image_list.append(img_tag)

        img_tags = self.soup.select("ul#J_UlThumb li a img")
        for op in img_tags:
            try:
                img_src = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError:
                img_src = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if img_src in image_list:
                continue
            if not img_src.startswith('http') and not img_src.startswith(
                'https'):
                img_src = "https:" + img_src
            image_list.append(img_src)
        image_list = list(set(image_list))
        self._images = image_list
        if image_list:
            self._chief_image = image_list[0]
        return image_list

    @property
    def shop_link(self):
        shop_link_tags = ('a.slogo-shopname',
                          'a.enter-shop',
                          'input#J_ShopSearchUrl')
        for shop_link_tag_name in shop_link_tags:
            shop_link_tag = self.soup.select(shop_link_tag_name)
            if shop_link_tag:
                shop_link = shop_link_tag[0].attrs['href']
                if not shop_link:
                    shop_link = shop_link_tag[0].attrs['value']
                if shop_link.startswith('//'):
                    shop_link = 'http:' + shop_link
                return shop_link

        shop_id_tag = re.findall('shopId:"(\d+)', self.html_source)
        if len(shop_id_tag) > 0:
            shop_link = "http://shop" + shop_id_tag[0] + ".taobao.com"
            return shop_link
        return "http://chaoshi.tmall.com/"

    def fetch_html(self):
        tmall_header = {
            'Cookie': 'cna=C6IRC8X/ODgCAd6BFDvWbabx; swfstore=293511; whl=-1%260%260%260; CNZZDATA1000279581=2084491831-1431329588-http%253A%252F%252Fsubject.tmall.com%252F%7C1432794651; lzstat_uv=11965390701316469673|2934243@2674749@3576861; lzstat_ss=140379413_3_1398070003_2934243|815277699_0_1422723118_2674749|2999861223_2_1434841102_3576861; ucn=center; tkmb=e=zGU0g6e1d7xnyW5i7tVTF34AiQ6j29rfKzBnvRc7iWAKnIJfZf8qogh3jq5OecGVnIZVGJ6iJNJUooZBX7Ci3Kb86eKaBMLWSFMJq3gfdbiOtqM14m8TUixr3LK%2FQUevmmOcDn3qcCAD0AiwnIeHDgP50F2QwFA5ztriqzRqqT9%2Fh3aZffAL0k6U0Q%3D%3D&iv=0&et=1436260677; ck1=; _tb_token_=e3eab0131bee0; uc3=nk2=F5fFAGakplCe&id2=UU21bCqQ9jo%3D&vt3=F8dASM2ebvybuPH%2FldI%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=tayaktaka; tracknick=tayaktaka; cookie2=2c4c3d08862516f8b17f01d55c31d074; skt=7b0c61cad5da6b2f; t=5070ce985c3f11b15a524d6788515bf0; tk_trace=1; pnm_cku822=172UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktyTnpCdkJ%2BRXxIfSs%3D%7CU2xMHDJ7G2AHYg8hAS8WKQcnCU4nTGI0Yg%3D%3D%7CVGhXd1llXGVZbVVhVWlSa19qXWBCe05zR3xDf0p%2BS3JKcEl0QW85%7CVWldfS0TMw8wDzAQLg4gdlNlSx1L%7CVmhIGCEdPRwgFCsUNAgxDDAQLhsvFjYKPgE8HCAdKBU1CT0CPx8jHiYcShw%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; cq=ccp%3D1; l=AgkJbJ5afOfrqhFMGy4g0hBRmTtjVv2I; isg=E67B4BE00CF880E3F80FAD48EBEE149E',
            'Referer': 'http://detail.tmall.com/item.htm?id=44691754172',
            'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
        }
        html = ''
        with requests.Session() as s:
            r = s.get(self.link, verify=False, headers=tmall_header, cookies={})
            html = r.text
            self._headers = r.headers
            script_url = self.fix_script_url(
                self.extract_price_script_url(html))
            price_script_response = s.get(script_url, headers=tmall_header).text
            self._price = self.process_price_response(price_script_response)
        return r.headers, html

    def process_price_response(self, price_script_response):
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
                priceInfo = entity_info['defaultModel']['itemPriceResultDO'][
                    'priceInfo']
                for k, v in priceInfo.iteritems():
                    prices.append(priceInfo[k]['price'])
                    # may be there is multiple promotionList ... TODO
                    if priceInfo[k]['promotionList'] and len(
                        priceInfo[k]['promotionList']):
                        for promo in priceInfo[k]['promotionList']:
                            try:
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
                if len(prices) > 0:
                    price = min(map(float, prices))
                else:
                    price = 0
        else:
            price = 0
        return price

    def extract_price_script_url(self, html_str):
        reg = re.compile('url=\'(\S*)\'')
        m = reg.search(html_str)
        return m.group(1)

    def fix_script_url(self, script_url):
        script_url = script_url.replace('mdskip.taobao.com', 'mdskip.tmall.com')
        l = list()
        prepend = ''
        if not 'http:' in script_url:
            prepend = 'http:'
        l.append("callback=setMdskip")
        l.append("timestamp=%d" % int(time()))
        return "%s%s&%s" % (prepend, script_url, '&'.join(l))
