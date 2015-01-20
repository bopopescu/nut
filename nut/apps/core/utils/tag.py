# coding=utf8
# from time import time
from apps.core.models import Tag

from hashlib import md5
import time
import hmac


class TagParser():
    text_string = ""

    def __init__(self, text_sting):
        self.text_string = text_sting

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
        tags = []

        self.text_string += " "
        i_sharp_start = None
        i = 0
        # text_string_len = len(text_string)
        while i < len(self.text_string):
            if not self._is_in_tag_interval(self.text_string[i]):
                if i_sharp_start != None:
                    if i > i_sharp_start:
                        tag = self.text_string[i_sharp_start:i]
                        if tags.count(tag) == 0:
                            tags.append(tag)
                    i_sharp_start = None
            if self.text_string[i] == "#" or self.text_string[i] == u"＃":
                i_sharp_start = i + 1
            i += 1
        return tags


    def cal_tag_hash(cls, tag_hash_string):
        _hash = None
        while True:
            _time_stamp = str(int(time.time()))
            _message = tag_hash_string.encode("utf8") + _time_stamp
            _hash = hmac.new("guokutag", _message, md5).hexdigest()[0:8]
            try:
                Tag.objects.get(tag_hash=_hash)
            #     TagModel.objects.get(tag_hash = _hash)
            except Tag.DoesNotExist:
                break

        return _hash


__author__ = 'edison'
