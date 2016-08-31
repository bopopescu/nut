from django.forms import Form
from django import forms


class AlipayReturnForm(Form):
    is_success = forms.CharField()
    pass