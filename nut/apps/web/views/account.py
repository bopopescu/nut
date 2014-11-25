from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from apps.web.forms.account import UserSignInForm


def login(request, template='web/account/login.html'):

    if request.is_ajax():
        template = 'web/account/partial/ajax_login.html'


    if request.method == "POST":
        _forms = UserSignInForm(request=request, data=request.POST)
        if _forms.is_valid():
            _forms.login()

            return HttpResponseRedirect(reverse('web_selection'))
    else:
        _forms = UserSignInForm(request)

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


def logout(request):
    auth_logout(request)
    request.session.set_expiry(0)
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    return HttpResponseRedirect(next_url)

__author__ = 'edison'
