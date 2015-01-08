from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET

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
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        request.session['auth_next_url'] = next_url
    return HttpResponseRedirect(sina.get_login_url())


@require_GET
def auth_by_sina(request):
    code = request.GET.get("code", None)
    error_uri = request.GET.get('error_uri', None)
    if code:
        _sina_data = sina.get_auth_data(code)
        next_url = request.session.get('auth_next_url', reverse("web_selection"))

        try:
            weibo = Sina_Token.objects.get(sina_id = _sina_data['sina_id'])
        except Sina_Token.DoesNotExist:
            raise

        login_without_password(request, weibo.user)
        return HttpResponseRedirect(next_url)


__author__ = 'edison'
