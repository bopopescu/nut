# -*- coding: utf-8 -*-
#  for Wizard_CaptchaField -- begin --
from django.forms import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from captcha.fields import CaptchaField,CaptchaTextInput
from captcha.models import CaptchaStore,get_safe_now
from captcha.conf import settings as captcha_settings

from django import forms
from django.forms import CharField
# for Wizard_CaptchaField -- end --


class Wizard_CaptchaField(CaptchaField):

    def __init__(self, *args, **kwargs):
        fields = (
            CharField(show_hidden_initial=True),
            CharField(),
        )
        if 'error_messages' not in kwargs or 'invalid' not in kwargs.get('error_messages'):
            if 'error_messages' not in kwargs:
                kwargs['error_messages'] = {}
            kwargs['error_messages'].update({'invalid': _('Invalid CAPTCHA')})

        kwargs['widget'] = kwargs.pop('widget', CaptchaTextInput(
            output_format=kwargs.pop('output_format', None),
            id_prefix=kwargs.pop('id_prefix', None),
            attrs={'class':'captcha-input','placeholder':_('Captcha Code')}
        ))
        self.hashKey = None

        super(CaptchaField, self).__init__(fields,*args, **kwargs)


    def clean(self,value):
        super(CaptchaField, self).clean(value)
        response, value[1] = (value[1] or '').strip().lower(), ''
        CaptchaStore.remove_expired()
        if captcha_settings.CAPTCHA_TEST_MODE and response.lower() == 'passed':
            # automatically pass the test
            try:
                # try to delete the captcha based on its hash
                CaptchaStore.objects.get(hashkey=value[0]).delete()
            except CaptchaStore.DoesNotExist:
                # ignore errors
                pass
        elif not self.required and not response:
            pass
        else:
            # https://code.google.com/p/django-simple-captcha/issues/detail?id=4
            try:
                CaptchaStore.objects.get(response=response, hashkey=value[0], expiration__gt=get_safe_now())
                self.hashKey = value[0]
            except CaptchaStore.DoesNotExist:
                raise ValidationError(getattr(self, 'error_messages', {}).get('invalid', _('Invalid CAPTCHA')))
        return value

    # def __del__(self):
    #     # https://code.google.com/p/django-simple-captcha/issues/detail?id=4
    #     #  delete the captchaStore latter
    #     #  django will call __del__ immediatly
    #     pass