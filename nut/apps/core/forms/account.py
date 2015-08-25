# coding=utf-8
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.template.defaulttags import url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from apps.core.models import GKUser, User_Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, get_user_model

from captcha.fields import CaptchaField

class GuoKuUserSignInForm(forms.Form):

    error_messages = {
        'no_email': _('email is not exist'),
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


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Please Input Your Email"),
                             max_length=254,
                             widget=forms.TextInput(attrs={'class':'form-control'}),
                             help_text=_('please register email'))

    captcha = CaptchaField(label=_("Please Input Captcha"),)

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        # UserModel = get_user_model()

    def clean_email(self):
        _email = self.cleaned_data.get('email')
        UserModel = get_user_model()
        try:
            UserModel._default_manager.get(email=_email)
        except:
            raise forms.ValidationError(
                _('email is not exist')
            )
        return _email

    def save(self, template_invoke_name, domain_override=None, use_https=False,
             token_generator=default_token_generator,
             from_email=None, request=None):
        """Overrides method of parent. """
        user_model = get_user_model()
        email = self.cleaned_data["email"]
        active_users = user_model._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                domain = current_site.domain
            else:
                domain = domain_override
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            user = user
            token = token_generator.make_token(user)
            protocol = 'https' if use_https else 'http'
            mail_message = EmailMessage(to=(email,),
                                        from_email='hi@guoku.com')
            reverse_url = reverse('web_password_reset_confirm',
                                  kwargs={'uidb64': uid, 'token': token})
            reset_link = "{0:s}:{1:s}{2:s}".format(protocol, domain, reverse_url)
            sub_vars = {'%name%': (user.nickname,),
                        '%reset_link%': (reset_link,),
                        }
            mail_message.template_invoke_name = template_invoke_name
            mail_message.sub_vars = sub_vars
            mail_message.send()


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                    help_text=_('New password'))
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                    help_text=_('New password confirmation'))

    def __init__(self, user, *args, **kwargs):

        super(UserSetPasswordForm, self).__init__(user, *args, **kwargs)

__author__ = 'edison'
