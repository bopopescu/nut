from django import forms
from django.contrib.auth import get_user_model, authenticate
from apps.core.forms.account import GuoKuUserSignInForm, GuokuUserSignUpForm
from apps.mobile.models import Session_Key
from apps.core.utils.image import HandleImage


class MobileUserSignInForm(GuoKuUserSignInForm):

    api_key = forms.CharField(
        widget=forms.TextInput(),
    )

    def __init__(self, request, *args, **kwargs):

        super(MobileUserSignInForm, self).__init__(request, *args, **kwargs)
        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['email'].label:
            self.fields['email'].label = self.username_field.verbose_name

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.api_key = self.cleaned_data.get('api_key')
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

        session = Session_Key.objects.generate_session(
            user_id=self.get_user_id(),
            email=self.user_cache.email,
            api_key=self.api_key,
            username="guoku",
        )
        return session.session_key


class MobileUserSignUpForm(GuokuUserSignUpForm):

    api_key = forms.CharField(
        widget=forms.TextInput(),
    )

    image = forms.FileField(
        widget=forms.FileInput(),
        required=False,
    )

    def save(self):
        self.api_key = self.cleaned_data.get('api_key')
        self.user_cache = super(MobileUserSignUpForm, self).save()

        _avatar_file = self.cleaned_data.get('image')
        if _avatar_file:
            _image = HandleImage(image_file= _avatar_file)
            avatar_path_name = _image.avatar_save()

            self.user_cache.profile.avatar = avatar_path_name

            self.user_cache.profile.save()

        return self.user_cache


    def get_session(self):

        session = Session_Key.objects.generate_session(
            user_id=self.get_user_id(),
            email=self.user_cache.email,
            api_key=self.api_key,
            username="guoku",
        )
        return session.session_key


class MobileUserSignOutForm(forms.Form):

    session = forms.CharField(
        widget=forms.TextInput()
    )

    def logout(self):
        _session = self.cleaned_data.get('session')
        try:
            _session_obj = Session_Key.objects.get(session_key=_session)
            _session_obj.delete()
            return True
        except Session_Key.DoesNotExist:
            return False


__author__ = 'edison7500'
