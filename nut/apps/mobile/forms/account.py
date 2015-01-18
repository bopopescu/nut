from django import forms
from django.contrib.auth import get_user_model, authenticate
from apps.core.forms.account import GuoKuUserSignInForm
from apps.mobile.models import Session_Key



class MobileUserSignInForm(GuoKuUserSignInForm):

    api_key = forms.CharField(
        widget=forms.TextInput(),
    )

    def __init__(self, request, *args, **kwargs):

        # self.request = request
        # self.user_cache = None

        super(MobileUserSignInForm, self).__init__(request, *args, **kwargs)
        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['email'].label:
            self.fields['email'].label = self.username_field.verbose_name

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
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )



    def get_session(self):
        _api_key = self.cleaned_data.get('api_key')
        session = Session_Key.objects.generate_session(
            user_id=self.get_user_id(),
            email=self.user_cache.email,
            api_key=_api_key,
            username="guoku",
        )
        return session.session_key
    # def login(self):
    #     pass
    # def login(self):
    #     # pass
    #     _email = self.cleaned_data.get('email')
    #     _password = self.cleaned_data.get('password')
    #     _api_key = self.cleaned_data.get('api_key')

__author__ = 'edison7500'
