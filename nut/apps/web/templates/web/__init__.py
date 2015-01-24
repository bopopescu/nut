from django.views.defaults import server_error
from django.views.defaults import page_not_found
# from django.shortcuts import render_to_response
from django.views.generic import TemplateView

def page_error(request):
    return server_error(request, template_name='500.html')

def webpage_not_found(request):
    return page_not_found(request, template_name='404.html')


class AboutView(TemplateView):
    template_name = "about.html"

class Agreement(TemplateView):
    template_name = "agreement.html"

class JobsView(TemplateView):
    template_name = "jobs.html"

class FaqView(TemplateView):
    template_name = "base_faq.html"


class LinksView(TemplateView):
    template_name = "links.html"