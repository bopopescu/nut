from pprint import pprint

from django.core.urlresolvers import reverse
from django.test import  TestCase, RequestFactory
from apps.payment.views.web import WXPayNotifyView

from apps.payment.weixinpay.parser import WXResponseParser

class WXNotifyParserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request_url = reverse('wxpay_notify')
        self.data =  '<xml></xml>'

    def test_notify_request_view_return_fail(self):
        request = self.factory.post(self.request_url, self.data, 'text/xml')
        response = WXPayNotifyView.as_view()(request)
        pprint('******')
        pprint(dir(response))
        pprint(response.content)
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers.get('content-type'), ('Content-Type', 'text/xml'))
        # self.assertEqual('FAIL' in response.text, True)
        # self.assertEqual('sign failed' in response.text, True)

    def notify_request_view_return_success(TestCase):
        data = '''
        '<xml><return_code><![CDATA[SUCCESS]]></return_code>\n<return_msg><![CDATA[OK]]></return_msg>\n<appid><![CDATA[wx59118ccde8270caa]]></appid>\n<mch_id><![CDATA[1370426502]]></mch_id>\n<device_info><![CDATA[WEB]]></device_info>\n<nonce_str><![CDATA[sLfluOPwBJttQD9x]]></nonce_str>\n<sign><![CDATA[C24C4DA3D4600FF093FF2DC024090FDB]]></sign>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<prepay_id><![CDATA[wx201608171211078e41d66c140756362781]]></prepay_id>\n<trade_type><![CDATA[NATIVE]]></trade_type>\n<code_url><![CDATA[weixin://wxpay/bizpayurl?pr=ooOuwSS]]></code_url>\n</xml>'

        '''





