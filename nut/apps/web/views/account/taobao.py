from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.web.lib.account.taobao import get_login_url, get_auth_data
from apps.core.models import Taobao_Token
from apps.web.lib.account.utils import login_without_password
# from apps.core.utils.taobaoapi.utils import

from django.utils.log import getLogger

log = getLogger('django')


def login_by_taobao(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['next_url'] = next_url
    return HttpResponseRedirect(get_login_url())



def auth_by_taobao(request):

    code = request.GET.get("code", None)
    if code:
        _taobao_data = get_auth_data(code)
        next_url = request.session.get('next_url', reverse("web_selection"))
        log.info(_taobao_data)

        try:
            taobao = Taobao_Token.objects.get(taobao_id=_taobao_data['taobao_id'])
            taobao.screen_name = _taobao_data['screen_name']
            taobao.access_token = _taobao_data['access_token']
            taobao.expires_in = _taobao_data['expires_in']
            taobao.save()

            log.info(taobao.user)

            login_without_password(request, taobao.user)
            return HttpResponseRedirect(next_url)
        except Taobao_Token.DoesNotExist:
            pass

    return



def bind(request):

    return


def unbind(request):

    return

__author__ = 'edison'
