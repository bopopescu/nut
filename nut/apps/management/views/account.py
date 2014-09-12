from django.shortcuts import render_to_response
from django.template import RequestContext


def sign_in(request, template='management/account/signin.html'):


    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
