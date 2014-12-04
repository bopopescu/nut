from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from apps.core.models import GKUser, User_Profile
# from django.contrib.auth.tokens import default_token_generator

from django.utils.log import getLogger
log = getLogger('django')



class UserSignInForm(forms.Form):

    error_messages = {
        'invalid_login': _('email or password wrong'),
        'password_error': _('password error'),
        'no_cookies': _('no cookies'),
    }

    next = forms.CharField(required=False, widget=forms.HiddenInput())

    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _('email')}),
        help_text=_('')
    )
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': _('password')}),
        help_text=_(''),

    )


    def __init__(self, request, *args, **kwargs):

        self.request = request
        self.user_cache = None

        super(UserSignInForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['email'].label:
            self.fields['email'].label = self.username_field.verbose_name

    # def clean_email(self):
    #     _email = self.cleaned_data.get('email')
    #
    #
    #     return _email
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.next_url = self.cleaned_data.get('next')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login']
                )
        elif not self.user_cache.is_active:
            raise


    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                self.error_messages['no_cookies']
            )


    def login(self):
        auth_login(self.request, self.user_cache)
        # pass

    def get_next_url(self):

        if self.next_url:
            return self.next_url
        return reverse('web_selection')

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserSignUpForm(forms.Form):

    error_messages = {
        'duplicate_nickname': _("A user with that nickname already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    nickname = forms.CharField(
        label=_('nickname'),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nickname'}),
        help_text=_(''),
    )

    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'hi@guoku.com'}),
        help_text=_(''),
    )

    password = forms.CharField(
        label=_('password'),
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':_('password')}),
        help_text=_('')
    )
    confirm_password = forms.CharField(
        label=_('confirm password'),
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':_('confirm passsword')}),
        help_text=_(''),
    )

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)


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

    def clean_confirm_password(self):
        _password = self.cleaned_data.get('password')
        _confirm_password = self.cleaned_data.get('confirm_password')
        if _password and _confirm_password and _password != _confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return _confirm_password


# forget password
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),
                             max_length=254,
                             widget=forms.TextInput(attrs={'class':'form-control'}),
                             help_text=_('please register email'))

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
