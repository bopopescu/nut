from django import forms
from apps.core.models import GKUser, User_Profile
from apps.v4.models import APIWeChatToken, APISession_Key
# from apps.mobile.models import Session_Key


class WeChatForm(forms.Form):
    unionid = forms.CharField(
        widget=forms.TextInput(),

    )

    nickname = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )

    headimgurl = forms.URLField(
        widget=forms.URLInput(),
        required=False,
    )


class WeChatSignInForm(WeChatForm):

    api_key = forms.CharField(
        widget=forms.TextInput()
    )

    def clean(self):
        _unionid = self.cleaned_data.get('unionid')
        _nickname = self.cleaned_data.get('nickname')
        _headimgurl = self.cleaned_data.get('headimgurl')
        self.api_key = self.cleaned_data.get('api_key')

        try:
            self.weixin = APIWeChatToken.objects.get(unionid = _unionid)
        except APIWeChatToken.DoesNotExist:

            user_key = APIWeChatToken.generate(_unionid, _nickname)
            email = "%s@guoku.com" % user_key
            user_obj = GKUser.objects.create_user(email=email, password=None)
            User_Profile.objects.create(
                user=user_obj,
                nickname=user_key,
                avatar = _headimgurl,
            )
            self.weixin = APIWeChatToken.objects.create(
                user = user_obj,
                nickname = _nickname,
                unionid = _unionid,
            )
        # finally:
        #     return self.weixin

    def login(self):

        session = APISession_Key.objects.generate_session(
            user_id=self.weixin.user_id,
            email=self.weixin.user.email,
            api_key=self.api_key,
            username="guoku",
        )
        res = {
            'user':self.weixin.user.v3_toDict(),
            'session':session.session_key,
        }
        return res

__author__ = 'edison'
