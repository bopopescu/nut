# coding=utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from apps.core.models import GKUser, User_Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, get_user_model

# from captcha.fields import CaptchaField

from apps.core.tasks.edm import send_forget_password_mail


class APIUserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Please Input Your Email"),
                             max_length=254,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control'}),
                             help_text=_('please register email'),)
    # email.validators.append(validate_user_status)

    # if hasattr(settings, 'TESTING') and settings.TESTING:
    #     captcha = CaptchaField(label=_("Please Input Captcha"), required=False)
    # else:
    #     captcha = CaptchaField(label=_("Please Input Captcha"))
    #
    def __init__(self, *args, **kwargs):
        super(APIUserPasswordResetForm, self).__init__(*args, **kwargs)
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
            email__iexact=email, is_active__gte=GKUser.blocked)
        for user in active_users:
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                domain = current_site.domain
            else:
                domain = domain_override

            send_forget_password_mail(gk_user=user, domain=domain,
                                      template_invoke_name=template_invoke_name,
                                      token_generator=token_generator)
