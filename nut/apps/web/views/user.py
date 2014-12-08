from django.shortcuts import render_to_response
from django.template import RequestContext


def settings(request, template="web/user/settings.html"):
    _user = request.user


    return render_to_response(
        template,
        {
            'user':_user,
        },
        context_instance = RequestContext(request),
    )



__author__ = 'edison'
