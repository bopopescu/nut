from django import forms
from apps.core.models import Taobao_Token, GKUser, User_Profile
from apps.core.utils.taobaoapi.user import TaobaoOpenIsvUID
from apps.mobile.models import Session_Key

from hashlib import md5
from datetime import datetime
import time

from django.conf import settings

app_key = getattr(settings, 'BAICHUAN_APP_KEY', None)
app_secret = getattr(settings, 'BAICHUAN_APP_SECRET', None)


from django.utils.log import getLogger

log = getLogger('django')


class BaichuanForm(forms.Form):

    user_id = forms.CharField(
        widget=forms.TextInput()
    )

    nick = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )


class BaichuanSignInForm(BaichuanForm):

    api_key = forms.CharField(
        widget=forms.TextInput()
    )

    def clean(self):
        _user_id = self.cleaned_data.get('user_id')
        _nick = self.cleaned_data.get('nick')
        # _avatar = self.cleaned_data.get('avatar')
        self.api_key = self.cleaned_data.get('api_key')

        t = TaobaoOpenIsvUID(app_key, app_secret)
        isv_uid = t.get_isv_uid(_user_id)

        log.info("isv %s" % isv_uid)

        try:
            self.taobao = Taobao_Token.objects.get(isv_uid = isv_uid)
            return self.taobao
        except Taobao_Token.DoesNotExist:

            user_key = Taobao_Token.generate(_user_id, _nick)
            email = "%s@guoku.com" % user_key
            user_obj = GKUser.objects.create_user(email=email, password=None)
            User_Profile.objects.create(
                user=user_obj,
                nickname=_nick,
                # avatar=_avatar,
            )
            self.taobao = Taobao_Token.objects.create(
                user = user_obj,
                screen_name = _nick,
                isv_uid = isv_uid,
            )
            return self.taobao
            # raise forms.ValidationError(
            #     'token is note exist'
            # )

    def login(self):

        session = Session_Key.objects.generate_session(
            user_id=self.taobao.user_id,
            email=self.taobao.user.email,
            api_key=self.api_key,
            username="guoku",
        )
        res = {
            'user':self.taobao.user.v3_toDict(),
            'session':session.session_key,
        }

        return res


#
# def generate(user_id, nick):
#
#     code_string = "%s%s%s" % (user_id, nick, time.mktime(datetime.now().timetuple()))
#
#     return md5(code_string.encode('utf-8')).hexdigest()

__author__ = 'edison'
