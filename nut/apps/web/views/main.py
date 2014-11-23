from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView


def index(request):


    return HttpResponse("OK")


def selection(request, template='web/main/selection.html'):


    return render_to_response(
        template,
        {

        },

    )


def popular(request, template='web/main/popular.html'):


    return render_to_response(
        template,
        {

        },

    )

def search(request, template="web/main/search.html"):


    return render_to_response(
        template,
        {

        },

    )

class AboutView(TemplateView):
    template_name = "web/about.html"

class Agreement(TemplateView):
    template_name = "web/agreement.html"

class JobsView(TemplateView):
    template_name = "web/jobs.html"

class FaqView(TemplateView):
    template_name = "web/base_faq.html"

__author__ = 'edison'



