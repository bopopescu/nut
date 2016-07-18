#encoding=utf-8

from apps.payment.exceptions import PaymentException

class BasePayment(object):

    def __init__(self,order=None, host='http://www.guoku.com'):
        if order is None:
            return PaymentException('payment must be inited with order instance')
        self._order = order
        self._host  = host

    @property
    def payment_url(self):
        raise NotImplemented()

    @property
    def return_url(self):
        raise NotImplemented()

    @property
    def notify_url(self):
        raise NotImplemented()

    @property
    def refound_notify_url(self):
        raise NotImplemented()