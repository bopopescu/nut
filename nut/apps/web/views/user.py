from django.shortcuts import render_to_response
from django.template import RequestContext


def settings(request, template="web/user/settings.html"):

    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )


__author__ = 'edison'
