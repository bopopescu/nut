from django.shortcuts import render_to_response
from django.template import RequestContext



def detail(request, hash, template="web/tags/detail.html"):


    return render_to_response(
        template,
        {

        },
    )

__author__ = 'edison'
