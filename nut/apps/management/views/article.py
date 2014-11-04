from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.forms.article import CreateArticleForms


def create(request, template="management/article/create.html"):

    if request.method == "POST":
        _forms = CreateArticleForms(request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = CreateArticleForms()



    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


__author__ = 'edison'
