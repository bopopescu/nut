from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Banner

def list(request, template="management/banner/list.html"):

    page = request.GET.get('page', 1)
    banner_list = Banner.objects.all()

    paginator = Paginator(banner_list, 30)

    try:
        banners = paginator.page(page)
    except InvalidPage:
        banners = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
                    template,
                    {
                        'banners':banners,
                    },
                    context_instance = RequestContext(request)
                )

__author__ = 'edison'
