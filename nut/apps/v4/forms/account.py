from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from apps.core.forms.account import GuoKuUserSignInForm, GuokuUserSignUpForm
from apps.core.forms.weibo import WeiboForm
from apps.core.forms.taobao import TaobaoForm
from apps.core.models import Sina_Token, Taobao_Token,GKUser, User_Profile
from apps.mobile.models import Session_Key

from apps.core.utils.image import HandleImage
from apps.core.tasks.account import fetch_avatar, update_token
from apps.v4.models import APIWeiboToken
from django.utils.log import getLogger

log = getLogger('django')


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
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
    )
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


class MobileUserRestPassword(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
        required=False,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(),
        required=False,
    )

    def clean_email(self):
        _email = self.cleaned_data.get('email')

        if _email is None:
            return None

        if self.user_cache.email == _email:
            return _email

        try:
            get_user_model()._default_manager.get(email = _email)
        except get_user_model().DoesNotExist:
            return _email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code= 'duplicate_email',
        )

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(MobileUserRestPassword, self).__init__(*args, **kwargs)

    def save(self):
        _password = self.cleaned_data.get('password')
        _email = self.cleaned_data.get('email')
        if _email:
            self.user_cache.email = _email

        if _password:
            self.user_cache.set_password(_password)
            # self.user_cache.save()
        self.user_cache.save()
        return self.user_cache.v3_toDict()


class MobileUserUpdateEmail(forms.Form):

    error_messages = {
        'password_error': _('password error'),
        'duplicate_email': _("duplicate email"),
    }

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
        required=True,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(),
        required=True,
    )

    def clean_email(self):
        _email = self.cleaned_data.get('email')

        if _email is None:
            return None

        if self.user_cache.email == _email:
            return _email

        try:
            get_user_model()._default_manager.get(email = _email)
        except get_user_model().DoesNotExist:
            return _email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password(self):
        _password = self.cleaned_data.get('password')
        is_vaild = self.user_cache.check_password(_password)
        if not is_vaild:
            raise forms.ValidationError(
                self.error_messages['password_error'],
                code='password error',
            )
        return _password

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(MobileUserUpdateEmail, self).__init__(*args, **kwargs)

    def save(self):
        # _password = self.cleaned_data.get('password')
        _email = self.cleaned_data.get('email')

        if _email:
            self.user_cache.email = _email

        # if _password:
        #     self.user_cache.set_password(_password)
            # self.user_cache.save()
        self.user_cache.save()
        return self.user_cache.v3_toDict()



__author__ = 'edison7500'
