# -*- coding: UTF-8 -*-
import  random, string
from pprint import pprint
from urllib import urlencode
from hashlib import md5
import  requests
import xml.etree.cElementTree as ET

from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str, smart_unicode


from apps.payment.basepay import BasePayment
from apps.payment.weixinpay.config import WX_APPID, WX_KEY, WX_MCH_ID
from apps.payment.exceptions import PaymentException
from apps.payment.weixinpay.parser import WXResponseParser

class WXPayment(BasePayment):
    _GATEWAY = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def __init__(self, *args, **kwargs):
        super(WXPayment, self).__init__(*args, **kwargs)
        self._parser = WXResponseParser()

    def params_filter(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            # k = self.smart_str(k, 'utf-8')
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = self.smart_str(v, 'utf-8')
                # newparams[k] = v
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        # print(prestr)
        return newparams, prestr

    def get_prepay_id(self):
        headers = {'Content-Type':'application/xml'}
        response = requests.post(self._GATEWAY,
                                 data=self.get_request_xml_string(),
                                 headers=headers)
        return self._parse_prepay_id(response)

    def _parse_prepay_id(self, response):
        return self._parser.parse_key_from_response(response, 'prepay_id')


    def get_payment_qrcode_url(self):
        headers = {'Content-Type':'application/xml'}
        response = requests.post(self._GATEWAY,
                                 data=self.get_request_xml_string(),
                                 headers=headers)
        return self._parse_payment_url(response)

    def _parse_payment_url(self, response):
        return self._parser.parse_key_from_response(response,'code_url')


    def get_request_xml_string(self):
        root = ET.Element('xml')
        for k , v in self.get_request_params().iteritems():
            ET.SubElement(root, k).text = v
        return ET.tostring(root, encoding='utf8', method='xml')

    def get_rd_string(self, length=32):
        return ''.join(random.choice(string.lowercase) for i in range(length))


    def get_request_params(self):
        params = dict()
        params['appid'] = WX_APPID
        params['mch_id'] = WX_MCH_ID
        params['nonce_str'] = self.get_rd_string().upper()
        # params['body'] = self._order.payment_body
        params['body'] = 'payment_body'
        params['out_trade_no'] = self._order.number
        params['total_fee'] = self.get_wx_order_total_fee()
        params['spbill_create_ip'] = self.get_spbill_ip()
        params['notify_url'] = self._host + self.notify_url
        params['trade_type'] = 'NATIVE'
        params['device_info'] = 'WEB'

        params, prestr = self.params_filter(params)
        params['sign'] = self.build_sign(prestr,WX_KEY)
        return params

    def build_sign(self, prestr, api_key):
        signStringTemp = "%s&key=%s"%(prestr,api_key)
        # print(signStringTemp)
        _result= md5(signStringTemp).hexdigest().upper()
        # print(_result)
        return _result

    def get_wx_order_total_fee(self):
        # https://pay.weixin.qq.com/wiki/doc/api/native.php?chapter=4_2
        # value is cent , not dollar
        return int(self._order.order_total_value * 100)

    @property
    def notify_url(self):
        return reverse('wxpay_notify')

    def get_spbill_ip(self):
        return '114.113.154.46'






