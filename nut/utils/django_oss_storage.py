#!/usr/bin/env python
# coding=utf-8

from django.conf import settings
from django.core.files.storage import Storage
import oss2


class OSSStorage(Storage):

    def __init__(self):
        self.auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET)

    def _open(self, name, mode='rb'):
        return self.bucket.get_object(name)

    def _save(self, name, content):
        self.bucket.put_object(name, content)
        return name

    def listdir(self, path):
        pass

    def created_time(self, name):
        pass

    def url(self, name):
        pass

    def delete(self, name):
        pass

    def path(self, name):
        pass

    def accessed_time(self, name):
        pass

    def modified_time(self, name):
        pass

    def size(self, name):
        pass

    def exists(self, name):
        pass

