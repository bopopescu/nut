# -*- coding: utf-8 -*-

from django.utils.log import getLogger


log = getLogger('django')


class Fetcher(object):

    def __init__(self, entity_url):
        self.entity_url = entity_url

    def get_fetcher(self):
        pass
