from django import forms
from django.utils.translation import ugettext_lazy as _


class GuoKuUserSignInForm(forms.Form):

    email = forms.EmailField(
        label=_('email'),
    )

    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(),
        min_length=6,
        help_text=_('')
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(GuoKuUserSignInForm, self).__init__(*args, **kwargs)

__author__ = 'edison'
