from django.views.generic import TemplateView
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

class AboutView(TemplateView):
    template_name = "web/about.html"

class Agreement(TemplateView):
    template_name = "web/agreement.html"

class JobsView(TemplateView):
    template_name = "web/jobs.html"

class FaqView(TemplateView):
    template_name = "web/base_faq.html"

class LinksView(TemplateView):
    template_name = "web/links.html"


class DownloadView(TemplateView):
    template_name = "web/download.html"


def download_ios(request):

    return HttpResponsePermanentRedirect(reverse('web_download'))


__author__ = 'edison7500'
