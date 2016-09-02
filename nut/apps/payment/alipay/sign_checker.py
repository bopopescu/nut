import types
from hashlib import md5, sha1

import M2Crypto

from apps.payment.alipay.settings import alipay_settings


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
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
                    return ' '.join([smart_str(arg, encoding, strings_only,
                            errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s


def params_filter(params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = smart_str(k)
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = smart_str(v)
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr


def build_sign(prestr, key, sign_type='MD5'):
        if sign_type == 'MD5':
            return md5(prestr + key).hexdigest()
        elif sign_type == 'RSA':
            return rsa_sign(prestr)
        return ''


def rsa_sign(data, key=alipay_settings.ALIPAY_GK_RSA_PRIVATE):
    key = M2Crypto.RSA.load_key_string(key)
    m = M2Crypto.EVP.MessageDigest('sha1')
    m.update(data)
    digest = m.final()
    signature = key.sign(digest, "sha1")
    return signature


def get_sign_from_params(params, sign_type="MD5"):
        params, prestr = params_filter(params)
        return build_sign(prestr, alipay_settings.ALIPAY_KEY, sign_type=sign_type)


def check_sign(params, sign_type='MD5'):
        return params.get('sign', None) == get_sign_from_params(params, sign_type=sign_type)


