import json

from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.payment.weixinpay.config import WX_MCH_ID, WX_APPID
from apps.order.models import Order
from apps.order.exceptions import OrderException
from apps.payment.models import PaymentLog

class WXPaymentNotifyHanlder(object):
    def __init__(self, dic):
        self._dic = dic

    def handle_notify(self):
        if self.check_payment_success() and self.check_payment_account():
            self.update_order_status()
            self.write_payment_log()
        else :
            return

    def check_payment_success(self):
        if self._dic.get('result_code', 'FAIL') == 'SUCCESS' and self.check_payment_amount():
            return True
        else:
            return False

    def check_payment_account(self):
        mch_id  = self._dic.get('mch_id', None)
        app_id  = self._dic.get('appid', None)
        return mch_id == WX_MCH_ID and app_id == WX_APPID

    def update_order_status(self):
        _order = self.get_order()
        try :
            _order.set_paid()
        except OrderException as e :
            pass

    def check_payment_amount(self):
        _order = self.get_order()
        if _order is None:
            return False
        if _order.order_total_value != self._dic.get('total_fee', 0):
            return False
        return True


    def get_order(self):
        _order_num = self._dic.get('out_trade_no',None)
        try :
            _order = get_object_or_404(Order, number=_order_num)
        except Http404 as e:
            _order = None

        return _order

    def write_payment_log(self):
        _order = self.get_order()
        _plog, created = PaymentLog.objects.get_or_create(
            order = _order,
            payment_source = PaymentLog.weixin_pay,
        )

        if created :
            _plog.payment_status = PaymentLog.paid
            _plog.payment_notify_info = json.dumps(self._dic)
            _plog.pay_time = self._dic.get('time_end')
            _plog.save()
        return