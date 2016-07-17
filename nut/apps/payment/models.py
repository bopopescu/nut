from django.db import  models

from apps.order.models import Order


class PaymentLog(models.Model):
    '''
        a log for payment route
    '''
    (waiting_for_payment,
            paid, refund) = range(3)

    PAYMENT_STATUS_CHOICES = [
        (waiting_for_payment, _('waiting for payment')),
        (paid, _('paid')),
        (refund, _('refund')),
        ]
    order = models.ForeignKey('order.Order', related_name='payments')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES)
    created_datetime =  models.DateTimeField(auto_now_add=True)
    updated_datetime =  models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.order.order_total_value
