import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.log import getLogger

from apps.payment.weixinpay.config import WX_MCH_ID, WX_APPID
from apps.order.models import Order
from apps.order.exceptions import OrderException
from apps.payment.models import PaymentLog

log = getLogger('django')

class WXPaymentNotifyHanlder(object):
    def __init__(self, dic):
        # log.warning(json.dumps(dic))
        self._dic = dic

    def handle_notify(self):
        if self.check_payment_success() and self.check_payment_account():
            self.update_order_status()
            self.write_payment_log()
        else :
            return

    def check_payment_success(self):
        # log.warning('result_code: %s'%self._dic.get('result_code'))
        # log.warning('is result_code equal success ? ')
        # log.warning(self._dic.get('result_code', 'FAIL') == 'SUCCESS')
        #

        if self._dic.get('result_code', 'FAIL') == 'SUCCESS' and self.check_payment_amount():
            return True
        else:
            log.warning('wx pay notify result fail for order number : %s'\
                        %self._dic.get('out_trade_no'))
            return False

    def check_payment_account(self):
        mch_id  = self._dic.get('mch_id', None)
        app_id  = self._dic.get('appid', None)

        # log.warning('WX_APPID : %s'%WX_APPID)
        # log.warning('WX_MCH_ID : %s'%WX_MCH_ID)

        if not( mch_id == WX_MCH_ID and app_id == WX_APPID):
            log.warning('wx pay notify account error for order : %s' \
                        %self._dic.get('out_trade_no'))
            return False
        else :
            return True

    def update_order_status(self):
        _order = self.get_order()
        try :
            _order.set_paid()
        except OrderException as e :
            pass

    def check_payment_amount(self):
        _order = self.get_order()
        log.warning('order number %s'%_order.number)
        log.warning('_order total value : %s'%_order.order_total_value)
        log.warning('dic total_fee : %s'%self._dic.get('total_fee'))

        if _order is None:
            return False
        if float(_order.order_total_value*100) != float(self._dic.get('total_fee', 0)):
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
            payment_status = PaymentLog.paid
        )

        if created :
            _plog.payment_notify_info = json.dumps(self._dic)
            _plog.pay_time = self._dic.get('time_end')
            _plog.save()
            log.info('payment log created')
        return