from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordResetForm

from apps.web.forms.account import UserSignInForm


def login(request, template='web/account/login.html'):

    redirect_url = reverse('web_selection')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)

    if request.is_ajax():
        template = 'web/account/partial/ajax_login.html'


    if request.method == "POST":
        _forms = UserSignInForm(request=request, data=request.POST)
        if _forms.is_valid():
            _forms.login()
            next_url = _forms.get_next_url()
            return HttpResponseRedirect(next_url)
    else:
        _forms = UserSignInForm(request)

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request),
    )


def register(request, template='web/account/register.html'):


    return  render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )


def logout(request):
    auth_logout(request)
    request.session.set_expiry(0)
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    return HttpResponseRedirect(next_url)


def forget_password(request, template='web/account/forget_password.html'):

    if request.method == 'POST':
        _forms = PasswordResetForm(request.POST)
        if _forms.is_valid():
            _forms.save(domain_override='guoku.com')

    else:
        _forms = PasswordResetForm()


    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison'
