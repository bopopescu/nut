from django.core.urlresolvers import reverse


class alipay_settings(object):

    ALIPAY_KEY = "uift5ax02scrpb5ce6nofju1da6skysk"
    ALIPAY_PARTNER = '2088422742956241'
    ALIPAY_INPUT_CHARSET = 'utf-8'
    ALIPAY_SELLER_EMAIL = 'anchen@guoku.com'
    ALIPAY_SIGN_TYPE = 'MD5'
    ALIPAY_SHOW_URL = ''
    ALIPAY_TRANSPORT = 'https'
    ALIPAY_GK_RSA_PRIVATE = '''-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDvCAncBtFX1ds+olA6NmVhU/S1Mfq7RxzTNtfCWWk+GVEyzQfX
G3G3eLLUNXecRTYXs/TIeuPTJ4tOm8GRjpGMHU75WJz4BoU6wofhy+H8LKcBlRyP
K7aISQ23oNFFisMiyz3gKPkaudJ+lOAu7zHYnBx3Mt/nLG4ebD769IBRAQIDAQAB
AoGBAO5eGs7zcZJhLqlwXgcfNcxwV+jV9Y8LJICxAUrLtTr7LlE1y6rEsIthbxxW
UXhiQMY0bFf8zPNGTRLQGqGYBiVBl3tniAp5l/VFnY2Hg+Wl2y0WlaHAlosFnKWP
iktBNezqQtoDmfBXU80MDg3pItRolEGtpSUbPNuHwD+qDc6RAkEA/Senoag7HCHn
JOA+mSurAwB5dcwlZ3dLq7HLCbJGCGIjEXYxLI1GJltw/oe06JYbTyjom5tIE4Ff
fHzevxmWNQJBAPG3v9XNGeJ8Tmlm3kJm++ieuqlJPlxWeW80n6GFfy8k+Cg+BGBX
hkbWu9y1H5B1drGfEZj+BG0vW0OtqlaWuR0CQHSi954It6s/h5K66ryBnRoV9uAq
PbWNBkVF9kkyZQfpx0R9Uyy2rnJvwQDUn6pltpFjRMCk67Fo8wiVM7+SV10CQQC6
HQ5TM7nzflztoSwPGrZp1RXKVL/0XwzfSDiFKIHWLfP5IE9EUv/ruVkqxjcIhrke
aGknUKbd3vG5eZVHWIQtAkEAyMT9QFkAG9pi/MAofMopP9M3b9Id5+OfUgTDMTbN
fwQ44XckqFyLZzzNRIBRhc/YG96hXMMfShfPM71ZZGOI6Q==
-----END RSA PRIVATE KEY-----'''

    ALIPAY_RSA_PUBLIC = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRAFljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQEB/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5KsiNG9zpgmLCUYuLkxpLQIDAQAB
-----END PUBLIC KEY-----'''

    @property
    def ALIPAY_NOTIFY_URL(self):
        return reverse('alipay_notify')

    @property
    def ALIPAY_RETURN_URL(self):
        return reverse('alipay_return')

    @property
    def ALIPAY_REFUND_NOTIFY_URL(self):
        return reverse('alipay_refund_notify')