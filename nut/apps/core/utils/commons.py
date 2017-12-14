# -*- coding: utf-8 -*-

import six

try:
    from django.conf import settings
except:
    import os
    import sys

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
    from django.conf import settings

from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import PasswordResetTokenGenerator

CURRENCY_KEY_FORMAT = 'currency.exchange.%s.CNY'


def currency_converting(convert_from, amount):
    raise NotImplementedError


def get_user_agent(request):
    if not request:
        return
    return request.META['HTTP_USER_AGENT']


def get_client_ip(request):
    if not request:
        return

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class VerifyUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):
        ts_b36 = int_to_base36(timestamp)
        key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

        value = (six.text_type(user.pk) + user.password +
                 six.text_type(timestamp))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)


verification_token_generator = VerifyUserTokenGenerator()
