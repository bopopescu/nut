from django.shortcuts import render_to_response
from django.template import RequestContext

def dashboard(request, template='management/dashboard.html'):


    return render_to_response(template,
                                {},
                                context_instance = RequestContext(request))


__author__ = 'edison7500'
