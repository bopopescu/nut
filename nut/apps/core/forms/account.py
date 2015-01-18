from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from apps.core.models import GKUser, User_Profile


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


class GuokuUserSignUpForm(forms.Form):

    error_messages = {
        'duplicate_nickname': _("A user with that nickname already exists."),
        'duplicate_email': _("A user with that email already exists."),
        # 'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(),
    )

    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(),
        min_length=8,
        help_text=_('')
    )

    nickname = forms.CharField(
        widget=forms.TextInput()
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(GuokuUserSignUpForm, self).__init__(*args, **kwargs)

    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        print _nickname
        try:
            User_Profile.objects.get(nickname = _nickname)
        except User_Profile.DoesNotExist:
            return _nickname
        raise forms.ValidationError(
            self.error_messages['duplicate_nickname'],
            code='duplicate_nickname',
        )

    def clean_email(self):
        _email = self.cleaned_data.get('email')
        # UserModel = get_user_model()
        try:
            GKUser.objects.get(email=_email)
        except GKUser.DoesNotExist:
            return _email
        raise forms.ValidationError(
               self.error_messages['duplicate_email'],
               code='duplicate_email',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    def save(self):
        _nickname = self.cleaned_data.get('nickname')
        _email = self.cleaned_data.get('email')
        _password = self.cleaned_data.get('password')

        self.user_cache = GKUser.objects.create_user(
            email=_email,
            password = _password,
            is_active=True,
        )

        User_Profile.objects.create(
            user = self.user_cache,
            nickname = _nickname,

        )
        return self.user_cache


__author__ = 'edison'
