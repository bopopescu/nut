from django import forms
from apps.core.forms.taobao import TaobaoForm
from apps.core.models import Taobao_Token, GKUser, User_Profile
from apps.mobile.models import Session_Key
from apps.core.utils.image import HandleImage
from apps.core.tasks.account import update_token


class MobileTaobaoSignUpForm(TaobaoForm):

    email = forms.EmailField(
        widget=forms.EmailInput()
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
    )

    nickname = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )

    api_key = forms.CharField(
        widget=forms.TextInput()
    )

    image = forms.FileField(
        widget=forms.FileInput(),
        required=False,
    )

    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        # print _nickname
        try:
            User_Profile.objects.get(nickname = _nickname)
        except User_Profile.DoesNotExist:
            return _nickname
        raise forms.ValidationError(
            'duplicate_nickname'
        )

    def clean_email(self):
        _email = self.cleaned_data.get('email')
        # UserModel = get_user_model()
        try:
            GKUser.objects.get(email=_email)
        except GKUser.DoesNotExist:
            return _email
        raise forms.ValidationError(
            'duplicate_email'
        )

    def save(self):
        self.api_key = self.cleaned_data.get('api_key')
        _nickname = self.cleaned_data.get('nickname')
        _email = self.cleaned_data.get('email')
        _password = self.cleaned_data.get('password')

        _taobao_id = self.cleaned_data.get('taobao_id')
        _taobao_token = self.cleaned_data.get('taobao_token')
        _screen_name = self.cleaned_data.get('screen_name')
        # _api_key = self.cleaned_data.get('api_key')

        self.user_cache = GKUser.objects.create_user(
            email=_email,
            password = _password,
            is_active=GKUser.active,
        )

        User_Profile.objects.create(
            user = self.user_cache,
            nickname = _nickname,
        )

        _avatar_file = self.cleaned_data.get('image')
        if _avatar_file:
            _image = HandleImage(image_file= _avatar_file)
            avatar_path_name = _image.avatar_save()

            self.user_cache.profile.avatar = avatar_path_name

            self.user_cache.profile.save()
        update_token.delay(user_id=self.user_cache.id,
                    taobao_id=_taobao_id,
                     screen_name=_screen_name,
                     access_token=_taobao_token,
                     expires_in=7200)

        return self.user_cache

    def get_session(self):

        session = Session_Key.objects.generate_session(
            user_id=self.user_cache.id,
            email=self.user_cache.email,
            api_key=self.api_key,
            username="guoku",
        )
        return session.session_key


class MobileTaobaoLoginForm(TaobaoForm):

    api_key = forms.CharField(
        widget=forms.TextInput()
    )

    def clean_taobao_id(self):
        _taobao_id = self.cleaned_data.get('taobao_id')

        try:
            taobao = Taobao_Token.objects.get(taobao_id = _taobao_id)
            return taobao
        except Taobao_Token.DoesNotExist:
            raise forms.ValidationError(
                'token is note exist'
            )

    def login(self):
        _taobao_token = self.cleaned_data.get('taobao_token')
        _api_key = self.cleaned_data.get('api_key')

        _taobao = self.cleaned_data.get('taobao_id')

        _taobao.access_token = _taobao_token
        _taobao.save()

        session = Session_Key.objects.generate_session(
            user_id=_taobao.user_id,
            email=_taobao.user.email,
            api_key=_api_key,
            username="guoku",
        )
        res = {
            'user':_taobao.user.v3_toDict(),
            'session':session.session_key,
        }

        return res

__author__ = 'edison'
