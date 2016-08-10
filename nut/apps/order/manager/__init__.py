import datetime
from django.db import models
from django.core.cache import cache

class OrderManager(models.Manager):
    def generate_order_number(self):

        key  = datetime.datetime.now().strftime("%Y_%m%d_%H%M")
        if cache.get(key) is None:
            cache.set(key, 1, timeout=61)
            count = 1
        else:
            count = cache.incr(key)
        return "%s_%s"%(key,count)

