from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from apps.core.models import GKUser
from apps.wechat.models import Token
from django.utils.log import getLogger

log = getLogger('django')


class WeChatBindForm(forms.Form):
    error_messages = {
        'invalid_login': _('email or password wrong'),
        'inactive': _("This account is inactive."),
        'password_error': _('password error'),
        # 'no_cookies': _('no cookies'),
    }

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
    def __init__(self, *args, **kwargs):

        # self.request = request
        self.user_cache = None

        super(WeChatBindForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['email'].label:
            self.fields['email'].label = self.username_field.verbose_name

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # self.next_url = self.cleaned_data.get('next')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login']
                )
            elif self.user_cache.is_active == GKUser.remove:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

    def bind(self, open_id):
        log.info("open id %s" % open_id)

        try:
            token = Token.objects.get(open_id = open_id)
        except Token.DoesNotExist:
            token = Token(
                user = self.user_cache,
                open_id = open_id
            )
            token.save()
        return token



__author__ = 'edison7500'
