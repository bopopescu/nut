from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Banner, Show_Banner
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.core.forms.banner import CreateBannerForm, EditBannerForm

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


    if request.method == "POST":
        _forms = CreateBannerForm(request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = CreateBannerForm()

    return render_to_response(
                    template,
                    {
                        'forms': _forms,
                    },
                    context_instance = RequestContext(request) )

def edit(request, banner_id, template='management/banner/edit.html'):

    try:
        _banner = Banner.objects.get(pk = banner_id)
    except Banner.DoesNotExist:
        raise Http404

    data = {
        'content_type': _banner.content_type,
        'key': _banner.key,
    }

    if request.method == "POST":
        _forms = EditBannerForm(_banner, request.POST, request.FILES)

    else:
        _forms = EditBannerForm(_banner, data=data)


    return render_to_response(
        template,
        {
            'banner': _banner,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )



__author__ = 'edison'
