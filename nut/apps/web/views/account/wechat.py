# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

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
    r.encoding = 'utf8'
    return r.json()


def get_weixin_auth_url():

    data = {
        'appid': APPID,
        'redirect_uri': RedirectURI,
        'response_type': 'code',
        'scope': 'snsapi_login',
        'state': 'wechat',
    }

    url = "https://open.weixin.qq.com/connect/qrconnect?%s" % urlencode(data)

    return url

def login_by_wechat(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['next_url'] = next_url

    # data = {
    #     'appid': APPID,
    #     'redirect_uri': RedirectURI,
    #     'response_type': 'code',
    #     'scope': 'snsapi_login',
    #     'state': 'wechat',
    # }
    #
    # url = "https://open.weixin.qq.com/connect/qrconnect?%s" % urlencode(data)
    # print url
    return HttpResponseRedirect(get_weixin_auth_url())


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
        # r.encoding = 'utf-8'
        # log.error("encoding ==> %s" % AccessTokenURL)
        r.encoding = 'utf8'
        res = r.json()
        log.error(res)
        try:
            weixin = WeChat_Token.objects.get(unionid=res['unionid'])
            login_without_password(request, weixin.user)
            return HttpResponseRedirect(next_url)
        except WeChat_Token.DoesNotExist:
            weixinUserDict = get_user_info(access_token=res['access_token'], openid=res['openid'])

            is_bind = request.session.get('is_bind', None)
            if request.user.is_authenticated() and is_bind:
                # del request.session['next_url']
                print weixinUserDict
                del request.session['is_bind']
                WeChat_Token.objects.create(
                    user = request.user,
                    unionid = weixinUserDict['unionid'],
                    nickname = weixinUserDict['nickname'],
                )
                return HttpResponseRedirect(next_url)

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

@require_GET
@login_required
def bind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    # next_url = reverse('web_selection')
    if next_url:
        log.info(next_url)
        request.session['next_url'] = next_url
        request.session['is_bind'] = True
        return HttpResponseRedirect(get_weixin_auth_url())

    raise Http404

@require_GET
@login_required
def unbind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url is None:
        raise Http404
    try:
        token = WeChat_Token.objects.get(user=request.user)
    except WeChat_Token.DoesNotExist:
        raise Http404

    token.delete()
    return HttpResponseRedirect(next_url)
__author__ = 'edison'
