import requests
from bs4 import BeautifulSoup
from urlparse import urlparse, urljoin
from hashlib import md5

try:
    from django.core.cache import cache
except Exception, e:
    print e.message


origin_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    # 'Referer': 'http://detail.tmall.com/item.htm?id=44691754172'
    }

class Spider(object):

    def __init__(self, url):
        # self._url = url
        self.urlobj = urlparse(url)
        # self.html = self.fetch_html(self.url)
        try:
            self.html = self.fetch_html_cache(self.url)
        except NameError:
            self.html = self.fetch_html(self.url)
        self.soup = BeautifulSoup(self.html, from_encoding="UTF-8")

    @property
    def origin_id(self):
        key = md5(self.url).hexdigest()
        return key

    @property
    def url(self):
        url = "http://%s%s" % (self.urlobj.hostname, self.urlobj.path)
        return url
        # url = urljoin(url, ' ')
        # return url.rstrip()
    #
    # @property
    # def buy_link(self):
    #     return "%s?%s" % (self.url, 'tag=guoku-23')

    @property
    def hostname(self):
        return self.urlobj.hostname

    def fetch_html_cache(self, url):
        key = md5(self.url).hexdigest()

        res = cache.get(key)
        if res:
            # log.info(res)
            self._headers = res['header']
            return res['body']

        try:
            f = requests.get(url, headers = origin_headers,)
        except Exception, e:
            # log.error(e.message)
            raise

        # f = requests.get(url)
        self._headers = f.headers

        res = f.content
        cache.set(key, {'body':res, 'header':self._headers})
        return res

    def fetch_html(self, url):
        f = requests.get(url)
        self._headers = f.headers
        res = f.content
        return res



__author__ = 'xiejiaxin'
