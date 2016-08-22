import json
from django.db import  models
from django.utils.translation import ugettext_lazy as _

from apps.core.base import BaseModel


class PaymentLog(BaseModel):
    '''
        a log for payment/refund route and its results
    '''
    (waiting_for_payment,
            paid, refund) = range(3)

    PAYMENT_STATUS_CHOICES = [
        (waiting_for_payment, _('waiting for payment')),
        (paid, _('paid')),
        (refund, _('refund')),
        ]
    (weixin_pay, ali_pay)= range(2)

    PAYMENT_SOURCE_CHOICES = [
        (weixin_pay, _('weixin payment')),
        (ali_pay, _('ali payment'))
    ]

    order = models.ForeignKey('order.Order', related_name='payments')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES)
    payment_source = models.IntegerField(choices=PAYMENT_SOURCE_CHOICES)
    payment_notify_info = models.TextField(null=True, blank=True)
    refund_notify_info = models.TextField(null=True, blank=True)
    pay_time = models.CharField(max_length=32, null=True, blank=True)
    created_datetime =  models.DateTimeField(auto_now_add=True)
    updated_datetime =  models.DateTimeField(auto_now=True)

    @property
    def payment_info(self):
        if self.payment_notify_info :
            return json.loads(self.payment_notify_info)

    @property
    def total_price(self):
        return self.order.order_total_value
