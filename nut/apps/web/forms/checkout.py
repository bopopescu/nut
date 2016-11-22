# encoding: utf-8

import json

from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from apps.payment.models import PaymentLog
from apps.order.models import Order


class CheckDeskOrderExpireForm(forms.Form):
    order_id = forms.IntegerField(required=True)

    def clean_order_id(self,):
        try:
            order_id = self.cleaned_data.get('order_id')
            order = get_object_or_404(Order, pk=order_id)
            return order_id
        except Exception as e:
            raise ValidationError(
                    _('order id validation fail %s' % e.message),
                    code='order_id_invalid',
                    params={'order_id': order}
            )

    def get_order(self):
        order_id = self.cleaned_data.get('order_id')
        return get_object_or_404(Order, pk=order_id)

    def save(self):
        _order = self.get_order()
        _order.set_expire(force=True)



class CheckDeskOrderPayForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CheckDeskOrderPayForm, self).__init__(*args, **kwargs)

    order_id = forms.IntegerField(required=True)
    payment_type = forms.ChoiceField(label=_('付款方式'), required=True, choices=PaymentLog.PAYMENT_SOURCE_CHOICES)
    payment_note = forms.CharField(required=False)

    def get_order(self):
        order_id = self.cleaned_data.get('order_id')
        return get_object_or_404(Order, pk=order_id)

    def clean_order_id(self,):
        try:
            order_id = self.cleaned_data.get('order_id')
            order = get_object_or_404(Order, pk=order_id)
            return order_id
        except Exception as e:
            raise ValidationError(
                    _('order id validation fail %s' % e.message),
                    code='order_id_invalid',
                    params={'order_id': order}
            )

    def clean(self):
        cleaned_data = super(CheckDeskOrderPayForm, self).clean()
        if self.cleaned_data.get('payment_type') is None:
            raise ValidationError(_('请选择付款方式'))
        payment_type = int(self.cleaned_data.get('payment_type'))
        payment_note = self.cleaned_data.get('payment_note')
        if payment_type == PaymentLog.other and len(payment_note) == 0:
            raise ValidationError(
                _('请填写 付款备注')
            )
        return cleaned_data

    def save(self):
        _order = self.get_order()
        _order.set_paid()
        self.write_payment_log()

    def write_payment_log(self):
        _order = self.get_order()
        _payment_log, created = PaymentLog.objects.get_or_create(
            order=_order,
            payment_source=self.cleaned_data['payment_type'],
            payment_status=PaymentLog.paid
        )
        if created:
            _payment_log.payment_notify_info = json.dumps(self.get_payment_info_dic())
            _payment_log.pay_time = datetime.now()
            _payment_log.payment_note = self.cleaned_data.get('payment_note')
            _payment_log.save()
        return

    def get_payment_info_dic(self):
        _order = self.get_order()
        return {
            'payment_method': 'check desk',
            'payment_operator_id': self.request.user.id,
            'payment_operator_nick': self.request.user.nick,
            'payment_operator_time': datetime.now().strftime('%Y:%M:%D %H:%M:%S'),
            'payment_total': _order.order_total_value,
            'payment_note': self.cleaned_data.get('payment_note')
        }




