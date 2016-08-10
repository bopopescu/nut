import  random, string

from apps.payment.basepay import BasePayment
from apps.payment.weixinpay.config import WX_APPID, WX_APPSEC, WX_MCH_ID

class WXPayment(BasePayment):
    def payment_url(self):
        pass

    def get_rd_string(self, length=32):
        return ''.join(random.choice(string.lowercase) for i in range(length))


    def get_request_params(self):
        params = dict()
        params['appid'] = WX_APPID
        params['mch_id'] = WX_MCH_ID
        params['nonce_str'] = self.ge_rd_string()
        params['body'] = self._order.payment_body



        pass



    def get_signed_params(self):
        pass





