from django.http import HttpResponseRedirect
from apps.web.lib.account.taobao import get_login_url
# from apps.core.utils.taobaoapi.utils import


def login_by_taobao(request):
    request.session['auth_source'] = "login"
    next_url = request.GET.get('next', None)
    if next_url:
        request.session['auth_next_url'] = next_url
    return HttpResponseRedirect(get_login_url())



def auth_by_taobao(request):


    return


__author__ = 'edison'
