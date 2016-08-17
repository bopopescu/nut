from django.test import TestCase
from apps.payment.weixinpay.parser import WXResponseParser


class WXNotifyParserResponseParseTest(TestCase):
    def setUp(self):
        self.xml_str = u'<xml><return_code><![CDATA[SUCCESS]]></return_code>\n<return_msg><![CDATA[OK]]></return_msg>\n<appid><![CDATA[wx59118ccde8270caa]]></appid>\n<mch_id><![CDATA[1370426502]]></mch_id>\n<device_info><![CDATA[WEB]]></device_info>\n<nonce_str><![CDATA[sLfluOPwBJttQD9x]]></nonce_str>\n<sign><![CDATA[C24C4DA3D4600FF093FF2DC024090FDB]]></sign>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<prepay_id><![CDATA[wx201608171211078e41d66c140756362781]]></prepay_id>\n<trade_type><![CDATA[NATIVE]]></trade_type>\n<code_url><![CDATA[weixin://wxpay/bizpayurl?pr=ooOuwSS]]></code_url>\n</xml>'
        self.bad_xml_str = u'<xml><return_code><![CDATA[SUCCESS]]></return_code>\n<return_msg><![CDATA[OK]]></return_msg>\n<appid><![CDATA[wx59118ccde8270caa]]></appid>\n<mch_id><![CDATA[1370426502]]></mch_id>\n<device_info><![CDATA[WEB]]></device_info>\n<nonce_str><![CDATA[sLfluOPwBJttQD9x]]></nonce_str>\n<sign><![CDATA[C34C4DA3D4600FF093FF2DC024090FDB]]></sign>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<prepay_id><![CDATA[wx201608171211078e41d66c140756362781]]></prepay_id>\n<trade_type><![CDATA[NATIVE]]></trade_type>\n<code_url><![CDATA[weixin://wxpay/bizpayurl?pr=ooOuwSS]]></code_url>\n</xml>'
        self.parser = WXResponseParser()

    def test_check_sign(self):
        params = self.parser.parse_string_xml_to_dic(self.xml_str)
        self.assertEqual(self.parser.check_params_sign(params),True)
        bad_params = self.parser.parse_string_xml_to_dic(self.bad_xml_str)
        self.assertEqual(self.parser.check_params_sign(bad_params), False)



