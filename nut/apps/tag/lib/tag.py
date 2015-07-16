# -*- coding: utf-8 -*-
from hashlib import md5
# from datetime import datetime
from django.utils.log import getLogger

log = getLogger('django')

class TagParser():
    text_string = ""

    def __init__(self, text_sting):
        self.text_string = text_sting.lower()
        self._tags = self.parse()

    def _is_in_tag_interval(self, ch):
        ch_unicode = ord(ch)
        if ch_unicode >= 19968 and ch_unicode <= 40895:
            return True
        if ch_unicode >= 12352 and ch_unicode <= 12447:
            return True
        if ch_unicode >= 12448 and ch_unicode <= 12543:
            return True
        if ch_unicode >= 97 and ch_unicode <= 122:
            return True
        if ch_unicode >= 65 and ch_unicode <= 90:
            return True
        if ch_unicode >= 48 and ch_unicode <= 57:
            return True
        return False

    def parse(self):
        tag_list = list()

        self.text_string += " "
        i_sharp_start = None
        i = 0
        # text_string_len = len(text_string)
        while i < len(self.text_string):
            if not self._is_in_tag_interval(self.text_string[i]):
                if i_sharp_start != None:
                    if i > i_sharp_start:
                        tag = self.text_string[i_sharp_start:i]
                        if tag_list.count(tag) == 0:
                            tag_list.append(tag)
                    i_sharp_start = None
            if self.text_string[i] == "#" or self.text_string[i] == u"＃":
                i_sharp_start = i + 1
            i += 1
        return tag_list

    @property
    def tags(self):
        res = dict()
        for row in self._tags:
            res.update(
                {
                    row: md5(row.encode('utf-8')).hexdigest()
                }
            )
        return res

    @property
    def thashs(self):
        _hash = list()
        for row in self._tags:
            _hash.append(md5(row.encode('utf-8')).hexdigest())
        return _hash

__author__ = 'edison'
