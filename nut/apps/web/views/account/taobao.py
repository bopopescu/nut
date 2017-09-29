# coding=utf-8
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from apps.web.lib.account.taobao import get_login_url, get_auth_data
from apps.core.models import Taobao_Token, GKUser, User_Profile
from apps.web.lib.account.utils import login_without_password

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
            taobao = Taobao_Token.objects.get(isv_uid=_taobao_data['isv_uid'])
            taobao.taobao_id = _taobao_data['taobao_id']
            taobao.screen_name = _taobao_data['screen_name']
            taobao.access_token = _taobao_data['access_token']
            taobao.access_token = _taobao_data['refresh_token']
            taobao.expires_in = _taobao_data['expires_in']
            taobao.open_uid = _taobao_data['open_uid']
            taobao.save()

            login_without_password(request, taobao.user)
            return HttpResponseRedirect(next_url)
        except Taobao_Token.DoesNotExist:
            is_bind = request.session.get('is_bind', None)
            if request.user.is_authenticated() and is_bind:
                del request.session['is_bind']
                Taobao_Token.objects.create(
                    user=request.user,
                    taobao_id=_taobao_data['taobao_id'],
                    screen_name=_taobao_data['screen_name'],
                    access_token=_taobao_data['access_token'],
                    refresh_token=_taobao_data['refresh_token'],
                    expires_in=_taobao_data['expires_in'],
                    open_uid=_taobao_data['open_uid'],
                    isv_uid=_taobao_data['isv_uid'],
                )
                return HttpResponseRedirect(next_url)
            else:
                user_key = Taobao_Token.generate(_taobao_data['open_uid'], _taobao_data['screen_name'])
                email = "%s@guoku.com" % user_key
                user_obj = GKUser.objects.create_user(email=email, password=None)
                User_Profile.objects.create(
                    user=user_obj,
                    nickname=user_key,
                )
                Taobao_Token.objects.create(
                    user=user_obj,
                    taobao_id=_taobao_data['taobao_id'],
                    screen_name=_taobao_data['screen_name'],
                    access_token=_taobao_data['access_token'],
                    refresh_token=_taobao_data['refresh_token'],
                    expires_in=_taobao_data['expires_in'],
                    open_uid=_taobao_data['open_uid'],
                    isv_uid=_taobao_data['isv_uid'],
                )
                login_without_password(request, user_obj)
                return HttpResponseRedirect(next_url)


def bind(request):
    next_url = request.META.get('HTTP_REFERER', None)

    if next_url:
        request.session['next_url'] = next_url
        request.session['is_bind'] = True
        return HttpResponseRedirect(get_login_url())
    raise Http404


def unbind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url is None:
        raise Http404

    try:
        token = Taobao_Token.objects.get(user=request.user)
    except Taobao_Token.DoesNotExist:
        raise Http404
    token.delete()

    return HttpResponseRedirect(next_url)
