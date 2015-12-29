# -*- coding: utf-8 -*-

import re

from apps.core.fetch import get_key
from apps.core.fetch import clean_price_string
from apps.core.fetch.fetcher import Fetcher
from apps.core.utils.commons import currency_converting


class Amazon(Fetcher):
    def __init__(self, entity_url):
        Fetcher.__init__(self, entity_url)
        self.high_resolution_pattern = re.compile('hiRes"[\s]*:[\s]*"([^";]+)')
        self.large_resolution_pattern = re.compile('large"[\s]*:[\s]*"([^";]+)')
        self.price_pattern = re.compile(u'(?:￥|\$)\s?(?P<price>\d+\.\d+)')
        self.foreign_price = 0.0
        self.entity_url = entity_url
        self.origin_id = self.get_origin_id
        self.expected_element = self.get_expected_element()
        self.shop_link = self.hostname
        self.nick = self.get_nick()

    @property
    def get_origin_id(self):
        parts = self.entity_url.split('/')
        if u'product' in parts:
            return parts[parts.index(u'product') + 1]
        if u'dp' in parts:
            return parts[parts.index(u'dp') + 1]

    @property
    def desc(self):
        _desc = self.soup.select("#productTitle")
        if len(_desc):
            return _desc[0].string
        _desc = self.soup.title.string.split(':')
        return _desc[0]

    def get_nick(self):
        return get_key(self.hostname)

    def get_expected_element(self):
        if self.hostname.endswith('cn'):
            return 'div#centerCol'
        elif self.hostname.endswith('au'):
            return 'div.buying'
        elif self.hostname.endswith('br'):
            return 'div#divsinglecolumnminwidth'
        return 'body'

    @property
    def cid(self):
        cate = self.soup.select(
                "#wayfinding-breadcrumbs_feature_div .a-link-normal")
        if len(cate) > 0:
            href = cate[0].attrs.get('href')
            return href.split('=')[-1]
        return 0

    @property
    def price(self):
        return self._get_price()

    def _get_price(self):
        """ Get lowest price and converting currency.
        """
        price = 0.0
        prices = self._get_prices()
        if not prices:
            return price

        if len(prices) > 1:
            prices.sort()
        origin_price = prices[0]
        if not self.hostname.endswith('.cn'):
            cny_price = 0
            self.foreign_price = origin_price
            if self.hostname.endswith('.com'):
                cny_price = currency_converting('USD', origin_price)
            elif self.hostname.endswith('.jp'):
                cny_price = currency_converting('JPY', origin_price)
            return cny_price
        return origin_price

    def _get_prices(self):
        """ Find all tags of price.
        """
        prices = []

        # normal price tags
        price_tags = (
            'span#priceblock_ourprice',
            '#priceblock_dealpric',
            '#priceblock_saleprice',
            '#soldByThirdParty span',
            'span#ags_price_loca',
            'b.priceLarge',
            'div#soldByThirdParty > span.a-color-price'
        )
        for tag_name in price_tags:
            price_tags = self.soup.select(tag_name)
            if price_tags:
                prices_list = [clean_price_string(price_tag.text) for
                               price_tag in price_tags]
                prices_list = [tag for tag in prices_list if tag]
                prices.extend(prices_list)
                break

        # some special tags
        if not prices:
            price_tag = self.soup.select("table.product, div#tmmSwatches ul")
            if price_tag:
                price_tags = self.price_pattern.findall(price_tag[0].text,
                                                        re.MULTILINE)
                prices.extend(clean_price_string(price_tags))
        return prices

    @property
    def link(self):
        link = "http://%s/dp/%s" % (self.hostname, self.origin_id)
        return link

    @property
    def images(self):
        images = []
        image_js = self.soup.select("div#imageBlock_feature_div")
        if image_js:
            hires_images = self.high_resolution_pattern.findall(
                    image_js[0].text)
            if hires_images:
                images = hires_images
            else:
                large_images = self.large_resolution_pattern.findall(
                        image_js[0].text)
                if large_images:
                    images = large_images
        else:
            images = self.get_medium_images()
        return images

    def get_medium_images(self):
        images = list()
        optimages = self.soup.select("#altImages ul .a-list-item span img")
        # return opt
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#imageBlockThumbs div img")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                if len(img_link) == 0:
                    continue
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

        optimages = self.soup.select("#main-image")
        if len(optimages) > 0:
            for row in optimages:
                img_link = row.attrs.get('src')
                array = img_link.split('_')
                res = "%s%s" % (array[0], array[-1])
                images.append(res.replace('..', '.'))
            return images

    @property
    def brand(self):
        optbrands = self.soup.select('#brandByline_feature_div div a')
        if optbrands:
            try:
                brand = optbrands[0].string
                return brand
            except IndexError:
                return ''
        else:
            another_try = self.soup.select("a#brand")
            if another_try:
                return another_try[0]

