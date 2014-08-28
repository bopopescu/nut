from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Banner, Show_Banner
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage

def list(request, template="management/banner/list.html"):

    page = request.GET.get('page', 1)

    show_banners = Show_Banner.objects.all()[0:4]

    banner_list = Banner.objects.all()
    paginator = ExtentPaginator(banner_list, 30)

    try:
        banners = paginator.page(page)
    except InvalidPage:
        banners = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
                    template,
                    {
                        'banners': banners,
                        'show_banners': show_banners,
                    },
                    context_instance = RequestContext(request)
                )


def create(request, template='management/banner/create.html'):


    return render_to_response()

__author__ = 'edison'
