from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse



from django.utils.log import getLogger

log = getLogger('django')


APPID = 'wx59118ccde8270caa'


def login_by_wechat(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['next_url'] = next_url

    url = "https://open.weixin.qq.com/connect/qrconnect?appid=%s&redirect_uri=http://guoku.com/&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect" % APPID
    return HttpResponseRedirect(url)


def auth_by_wechat(request):


    return

__author__ = 'edison'
