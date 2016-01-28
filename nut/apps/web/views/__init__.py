from django.views.generic import TemplateView
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import redirect,render

from django.views.defaults import server_error
from django.views.defaults import page_not_found
from django.utils.log import getLogger

log = getLogger('django')

def page_error(request):
    return server_error(request, template_name='web/500.html')

def webpage_not_found(request):
    return page_not_found(request, template_name='web/404.html')


# class TestView(TemplateView):
#     template_name = 'web/index.html'

class HappyNYView(TemplateView):
    template_name = 'web/happynewyear/happy.html'

class AboutView(TemplateView):
    template_name = "web/about.html"

class Agreement(TemplateView):
    template_name = "web/agreement.html"

class JobsView(TemplateView):
    template_name = "web/jobs.html"

class FaqView(TemplateView):
    template_name = "web/base_faq.html"

class LinksView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(LinksView, self).get_context_data(**kwargs)
        return  context
    template_name = "web/links.html"


class DownloadView(TemplateView):
    template_name = "web/download.html"

    def get(self, request, *args, **kwargs):
        log.info(request.META['HTTP_USER_AGENT'])
        if  'MicroMessenger' in request.META['HTTP_USER_AGENT']:
            if 'iPhone' in request.META['HTTP_USER_AGENT']:
                template_name='web/jump_apple.html'
                return  render(request,template_name)
            else:
                return HttpResponseRedirect('http://a.app.qq.com/o/simple.jsp?pkgname=com.guoku')
        elif 'iPhone' in request.META['HTTP_USER_AGENT']:
            template_name='web/jump.html'
            return render(request,template_name)
            # return HttpResponseRedirect("http://itunes.apple.com/cn/app/id477652209")
        elif 'iPad' in request.META['HTTP_USER_AGENT']:
            return HttpResponseRedirect("http://itunes.apple.com/cn/app/id450507565?mt=8")
        elif 'Android' in request.META['HTTP_USER_AGENT']:
            return HttpResponseRedirect("http://app.guoku.com/download/android/guoku-release.apk")
        else:
            return super(DownloadView, self).get(request, *args, **kwargs)


def download_ios(request):

    return HttpResponsePermanentRedirect(reverse('web_download'))


__author__ = 'edison7500'
