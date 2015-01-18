from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login




class GuoKuUserSignInForm(forms.Form):

    error_messages = {
        'invalid_login': _('email or password wrong'),
        'inactive': _("This account is inactive."),
        'password_error': _('password error'),
        'no_cookies': _('no cookies'),
        'no_api_key': _('no guoku api key')
    }

    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(),
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

    def login(self):
        auth_login(self.request, self.user_cache)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

__author__ = 'edison'
