from django import forms
from django.utils.translation import gettext_lazy as _


class WeChatBindForm(forms.Form):
    email = forms.CharField(
        label=_('email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':_('email')}),
    )
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':_('password')}),
    )
    # open_id = forms.CharField(
    #     widget=forms.HiddenInput(),
    # )

    def bind(self, open_id):


        return



__author__ = 'edison7500'
