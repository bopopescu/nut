from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.web.forms.account import UserSignInForm


def login(request, template='web/account/login.html'):

    if request.is_ajax():

        template = 'web/account/partial/ajax_login.html'


    if request.method == "POST":
        _forms = UserSignInForm(request=request, data=request.POST)
        if _forms.is_valid():
            _forms.login()

            return
    else:
        _forms = UserSignInForm(request)

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
