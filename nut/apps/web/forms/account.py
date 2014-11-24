from django import forms
from django.utils.translation import gettext_lazy as _


class UserSignInForm(forms.Form):
    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('')
    )
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text=_(''),

    )


    # def save(self):
    def login(self):

        pass

__author__ = 'edison'
