#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from django.conf import settings


r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


class BaseHandler(object):

    def __init__(self):
        pass
