from django.db import models

class OrderManager(models.Manager):
    def generate_order_number(self):
        raise NotImplemented()

