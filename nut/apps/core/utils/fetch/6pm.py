from spider import Spider
from hashlib import md5

class SixPM(Spider):

    def __init__(self, url):
        super(SixPM, self).__init__(url)


    @property
    def origin_id(self):
        key = md5(self.url).hexdigest()
        return key

__author__ = 'edison'
