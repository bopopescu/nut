from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from apps.core.models import Sina_Token
# from apps.web.forms.account import UserSignInForm, UserPasswordResetForm
from apps.web.lib.account import sina
from apps.web.lib.account.utils import login_without_password
from django.utils.log import getLogger

log = getLogger('django')


@require_GET
def login_by_sina(request):
    request.session['auth_source'] = "login"
    # next_url = request.GET.get('next', None)
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    if 'login' in next_url:
        next_url = reverse('web_selection')
    log.info(next_url)
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
        del request.session['next_url']

        try:
            weibo = Sina_Token.objects.get(sina_id = _sina_data['sina_id'])
        except Sina_Token.DoesNotExist:
            raise

        log.info(_sina_data)

        is_bind = request.session.get('is_bind', None)
        if request.user.is_authenticated() and is_bind:
            del request.session['next_url']
            del request.session['is_bind']
            Sina_Token.objects.create(
                user = request.user,
                sina_id =  _sina_data['sina_id'],
            )
            return HttpResponseRedirect(next_url)

        if weibo.user_id:
            login_without_password(request, weibo.user)

            return HttpResponseRedirect(next_url)


@require_GET
@login_required
def bind(request):
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    if next_url:
        log.info(next_url)
        request.session['next_url'] = next_url
        request.session['is_bind'] = True
    else:
        raise Http404
    return HttpResponseRedirect(sina.get_login_url())


@require_GET
@login_required
def unbind(request):
    next_url = request.META.get('HTTP_REFERER', None)
    # if next_url is None:
    #     raise Http404

    try:
        token = Sina_Token.objects.get(user=request.user)
    except Sina_Token.DoesNotExist:
        raise Http404

    token.delete()
    return Http404(next_url)


__author__ = 'edison'
