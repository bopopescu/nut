# coding=utf-8
from django import http
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from django.utils.log import getLogger
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from django.template import loader, TemplateDoesNotExist, Template, RequestContext

log = getLogger('django')


def page_error(request):
    template_name = 'web/500.html'

    # safe init a context
    r_context = None
    try:
        r_context = RequestContext(request, {'request_path': request.path})
    except Exception as e:
        pass

    # try to load template
    try:
        template = loader.get_template(template_name)
        content_type = None  # Django will use DEFAULT_CONTENT_TYPE
    except TemplateDoesNotExist:
        template = Template(
            '<h1>Server Error</h1>'
            '<p></p>')
        content_type = 'text/html'

    # put them together
    body = template.render(r_context)
    return http.HttpResponseServerError(body, content_type=content_type)


def webpage_not_found(request):
    return page_not_found(request, template_name='web/404.html')


def permission_denied(request):
    return page_not_found(request, template_name='web/403.html')


class HappyNYView(TemplateView):

    template_name = 'web/happynewyear/happy.html'


class FuGuView(TemplateView):
    template_name = 'web/fugu/fugu2016.html'


class FuGuListView(TemplateView):
    template_name = 'web/fugu/fugu2016_list.html'


class MarketView(TemplateView):
    template_name = 'web/market/market2016.html'


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
        return context

    template_name = "web/links.html"


class ShopServiceView(TemplateView):
    template_name = 'web/shop_service.html'


class CooperateView(TemplateView):
    template_name = 'web/base_cooperate.html'


class DownloadView(TemplateView):
    template_name = "web/download.html"

    def get(self, request, *args, **kwargs):
        log.info(request.META['HTTP_USER_AGENT'])
        if 'MicroMessenger' in request.META['HTTP_USER_AGENT']:
            if 'iPhone' in request.META['HTTP_USER_AGENT']:
                template_name = 'web/jump_apple.html'
                return render(request, template_name)
            else:
                return HttpResponseRedirect('http://a.app.qq.com/o/simple.jsp?pkgname=com.guoku')
        elif 'iPhone' in request.META['HTTP_USER_AGENT']:
            template_name = 'web/jump.html'
            return render(request, template_name)
        elif 'iPad' in request.META['HTTP_USER_AGENT']:
            return HttpResponseRedirect("http://itunes.apple.com/cn/app/id450507565?mt=8")
        elif 'Android' in request.META['HTTP_USER_AGENT']:
            return HttpResponseRedirect("http://app.guoku.com/download/android/guoku-release.apk")
        else:
            return super(DownloadView, self).get(request, *args, **kwargs)


def download_ios(request):
    return HttpResponsePermanentRedirect(reverse('web_download'))
