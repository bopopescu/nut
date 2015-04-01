from django import forms

from apps.core.forms.weibo import WeiboForm
from apps.core.utils.image import HandleImage
from apps.core.models import Sina_Token, GKUser, User_Profile
from apps.mobile.models import Session_Key
from apps.core.tasks.account import update_token
from apps.v4.models import APIWeiboToken, APIUser
from django.utils.log import getLogger

log = getLogger('django')


class MobileWeiboSignUpForm(WeiboForm):

    email = forms.EmailField(
        widget=forms.EmailInput()
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
    )

    nickname = forms.CharField(
        widget=forms.TextInput()
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
            APIUser.objects.get(email=_email)
        except APIUser.DoesNotExist:
            return _email
        raise forms.ValidationError(
            'duplicate_email'
        )

    def save(self):
        self.api_key = self.cleaned_data.get('api_key')
        _nickname = self.cleaned_data.get('nickname')
        _email = self.cleaned_data.get('email')
        _password = self.cleaned_data.get('password')

        _weibo_id = self.cleaned_data.get('sina_id')
        _weibo_token = self.cleaned_data.get('sina_token')
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
                     weibo_id=_weibo_id,
                     screen_name=_screen_name,
                     access_token=_weibo_token,
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


class MobileWeiboLoginForm(WeiboForm):

    api_key = forms.CharField(
        widget=forms.TextInput()
    )

    def clean_sina_id(self):
        _weibo_id = self.cleaned_data.get('sina_id')

        try:
            weibo = Sina_Token.objects.get(sina_id = _weibo_id)
            return weibo
        except Sina_Token.DoesNotExist:
            raise forms.ValidationError(
                'token is not exist'
            )

    def login(self):
        _weibo_token = self.cleaned_data.get('sina_token')
        _screen_name = self.cleaned_data.get('screen_name')
        _api_key = self.cleaned_data.get('api_key')

        _weibo = self.cleaned_data.get('sina_id')

        _weibo.access_token = _weibo_token
        _weibo.screen_name = _screen_name
        _weibo.save()

        session = Session_Key.objects.generate_session(
            user_id=_weibo.user_id,
            email=_weibo.user.email,
            api_key=_api_key,
            username="guoku",
        )

        res = {
            'user':_weibo.user.v3_toDict(),
            'session':session.session_key,
        }

        return res

class MobileWeiboLinkForm(WeiboForm):

    user_id = forms.CharField(
        widget=forms.TextInput(),
    )

    expires_in = forms.IntegerField(
        widget=forms.NumberInput(),
    )

    def clean_sina_id(self):
        _sina_id = self.cleaned_data.get('sina_id')

        try:
            APIWeiboToken.objects.get(sina_id=_sina_id)
        except APIWeiboToken.DoesNotExist:
            return _sina_id
        raise forms.ValidationError(
            'already bind',
        )

    def save(self):
        _user_id = self.cleaned_data.get('user_id')
        _sina_id = self.cleaned_data.get('sina_id')
        _access_token = self.cleaned_data.get('sina_token')
        _screen_name = self.cleaned_data.get('screen_name')
        _expires_in = self.cleaned_data.get('expires_in')

        res = APIWeiboToken.objects.create(
            user_id = _user_id,
            sina_id = _sina_id,
            screen_name = _screen_name,
            expires_in = _expires_in,
            access_token = _access_token,
        )

        return res.user.v3_toDict()


class MobileWeiboUnLinkForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(),
    )
    sns_user_name = forms.CharField(
        widget=forms.TextInput(),
    )

    def clean(self):
        _user_id = self.cleaned_data.get('user_id')
        _weibo_name = self.cleaned_data.get('sns_user_name')

        try:
            self.weibo_cache =  Sina_Token.objects.get(user_id=_user_id, screen_name=_weibo_name)
        except Sina_Token.DoesNotExist:
            raise forms.ValidationError(
                'user is not exist'
            )

    def unlink(self):
        self.weibo_cache.delete()


__author__ = 'edison'
