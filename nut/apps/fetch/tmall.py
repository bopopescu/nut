# -*- coding: utf-8 -*-

import re

from urllib import unquote
from django.utils.log import getLogger

from apps.fetch.common import clean_price_string
from apps.fetch.base import BaseFetcher


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
        self.cid_pattern = re.compile(u'"rootCatId":"(?P<cid>\d*)')

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
        link = 'http://detail.tmall.com/item.htm?id=%s' % self.origin_id
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
        if seller_soup > 0:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()
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
            if "http" not in img_tag:
                img_tag = "http:" + img_tag
            if img_tag.startswith('//'):
                img_tag = 'http:'+img_tag
            image_list.append(img_tag)

        img_tags = self.soup.select("ul#J_UlThumb li a img")
        for op in img_tags:
            try:
                img_src = re.sub(IMG_POSTFIX, "", op.attrs.get('src'))
            except TypeError:
                img_src = re.sub(IMG_POSTFIX, "", op.attrs.get('data-src'))
            if img_src in image_list:
                continue
            if img_src.startswith('//'):
                img_src = 'http:'+img_src
            image_list.append(img_src)
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
            shop_link = "http://shop"+shop_id_tag[0]+".taobao.com"
            return shop_link
        return "http://chaoshi.tmall.com/"
