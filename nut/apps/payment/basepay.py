#encoding=utf-8
from hashlib import md5
import types

from apps.payment.exceptions import PaymentException

class BasePayment(object):

    def __init__(self,order=None, host='http://www.guoku.com'):
        if order is None:
            return PaymentException('payment must be inited with order instance')
        self._order = order
        self._host  = host


    def build_sign(self, prestr, key, sign_type = 'MD5'):
        if sign_type == 'MD5':
            return md5(prestr + key).hexdigest()
        return ''

    def params_filter(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = self.smart_str(k, 'utf-8')
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = self.smart_str(v, 'utf-8')
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr

    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Returns a bytestring version of 's', encoded as specified in 'encoding'.
        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    # An Exception subclass containing non-ASCII data that doesn't
                    # know how to print itself properly. We shouldn't raise a
                    # further exception.
                    return ' '.join([self.smart_str(arg, encoding, strings_only,
                            errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s


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