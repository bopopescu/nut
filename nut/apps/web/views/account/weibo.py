# coding=utf-8
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from apps.core.models import Sina_Token, GKUser, User_Profile
from apps.web.lib.account import sina
from apps.web.lib.account.utils import login_without_password
from django.utils.log import getLogger

log = getLogger('django')


@require_GET
def login_by_sina(request):
    request.session['auth_source'] = "login"
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    if 'login' in next_url:
        next_url = reverse('web_selection')
    if next_url:
        request.session['next_url'] = next_url
    return HttpResponseRedirect(sina.get_login_url())


@require_GET
def auth_by_sina(request):
    code = request.GET.get("code", None)
    error_uri = request.GET.get('error_uri', None)
    if code:
        _sina_data = sina.get_auth_data(code)
        next_url = request.session.get('next_url', reverse("web_selection"))
        try:
            weibo = Sina_Token.objects.get(sina_id=_sina_data['sina_id'])
            weibo.access_token = _sina_data['access_token']
            weibo.expires_in = _sina_data['expires_in']
            weibo.screen_name = _sina_data['screen_name']
            weibo.save()
            login_without_password(request, weibo.user)
            return HttpResponseRedirect(next_url)

        except Sina_Token.DoesNotExist:
            is_bind = request.session.get('is_bind', None)
            if request.user.is_authenticated() and is_bind:
                del request.session['is_bind']
                Sina_Token.objects.create(
                    user=request.user,
                    sina_id=_sina_data['sina_id'],
                    screen_name=_sina_data['screen_name'],
                    access_token=_sina_data['access_token'],
                    expires_in=_sina_data['expires_in'],
                )
                return HttpResponseRedirect(next_url)
            else:
                log.info(_sina_data)
                user_key = Sina_Token.generate(_sina_data['access_token'], _sina_data['screen_name'])
                email = "%s@guoku.com" % user_key
                user_obj = GKUser.objects.create_user(email=email, password=None)
                User_Profile.objects.create(
                    user=user_obj,
                    nickname=user_key,
                    avatar=_sina_data['avatar_large'],
                )
                Sina_Token.objects.create(
                    user=user_obj,
                    sina_id=_sina_data['sina_id'],
                    screen_name=_sina_data['screen_name'],
                    access_token=_sina_data['access_token'],
                    expires_in=_sina_data['expires_in'],
                )
                login_without_password(request, user_obj)
                return HttpResponseRedirect(next_url)
    else:
        log.error("%s", error_uri)
        return HttpResponse("error")


@require_GET
@login_required
def bind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url:
        log.info(next_url)
        request.session['next_url'] = next_url
        request.session['is_bind'] = True
        return HttpResponseRedirect(sina.get_login_url())

    raise Http404


@require_GET
@login_required
def unbind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url is None:
        raise Http404
    try:
        token = Sina_Token.objects.get(user=request.user)
    except Sina_Token.DoesNotExist:
        raise Http404

    token.delete()
    return HttpResponseRedirect(next_url)
