from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from urllib import urlencode
import requests

from apps.core.models import WeChat_Token, GKUser, User_Profile
from apps.web.lib.account.utils import login_without_password

from django.utils.log import getLogger

log = getLogger('django')


APPID = 'wx7b445b01ad2bfe9e'
APPSECRET = '37b28c446bd2187d99588ce85fc8b5a6'
RedirectURI = 'http://www.guoku.com/weixin/auth/'

AccessTokenURL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
UserInfoURL = 'https://api.weixin.qq.com/sns/userinfo'


def get_user_info(access_token, openid):

    r = requests.get(UserInfoURL, params = {
        'access_token': access_token,
        'openid': openid,
    })
    return r.json()



def login_by_wechat(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['next_url'] = next_url

    data = {
        'appid': APPID,
        'redirect_uri': RedirectURI,
        'response_type': 'code',
        'scope': 'snsapi_login',
        'state': 'wechat',
    }

    url = "https://open.weixin.qq.com/connect/qrconnect?%s" % urlencode(data)
    print url
    return HttpResponseRedirect(url)


def auth_by_wechat(request):

    code = request.GET.get('code', None)
    # access_token = request.GET.get('access_token', None)

    if code :
        next_url = request.session.get('next_url', reverse("web_selection"))
        data = {
            'appid': APPID,
            'secret': APPSECRET,
            # 'access_token': access_token,
            'code': code,
            'grant_type': 'authorization_code'
        }

        r = requests.get(AccessTokenURL, params=data)
        res = r.json()

        try:
            weixin = WeChat_Token.objects.get(unionid=res['unionid'])
            login_without_password(request, weixin.user)
            return HttpResponseRedirect(next_url)
        except WeChat_Token.DoesNotExist:
            weixinUserDict = get_user_info(access_token=res['access_token'], openid=res['openid'])

            user_key = WeChat_Token.generate(weixinUserDict['unionid'], weixinUserDict['nickname'])
            email = "%s@guoku.com" % user_key
            user_obj = GKUser.objects.create_user(email=email, password=None)
            User_Profile.objects.create(
                user=user_obj,
                nickname=user_key,
                avatar = weixinUserDict['headimgurl'],
            )
            WeChat_Token.objects.create(
                user = user_obj,
                unionid = weixinUserDict['unionid'],
                nickname = weixinUserDict['nickname'],
            )
            login_without_password(request, user_obj)
            return HttpResponseRedirect(next_url)
    else:
        raise Http404

__author__ = 'edison'
