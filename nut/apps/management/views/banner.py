from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.core.models import Banner, Show_Banner
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.core.forms.banner import CreateBannerForm, EditBannerForm
from apps.management.decorators import staff_only

from apps.core.views import LoginRequiredMixin
from django.views.generic import ListView

# @login_required
# @staff_only
# def list(request, template="management/banner/list.html"):
#
#     page = request.GET.get('page', 1)
#
#     show_banners = Show_Banner.objects.all()[0:4]
#
#     banner_list = Banner.objects.all()
#     paginator = ExtentPaginator(banner_list, 30)
#
#     try:
#         banners = paginator.page(page)
#     except InvalidPage:
#         banners = paginator.page(1)
#     except EmptyPage:
#         raise Http404
#
#     return render_to_response(
#                     template,
#                     {
#                         'banners': banners,
#                         'show_banners': show_banners,
#                     },
#                     context_instance = RequestContext(request)
#                 )

class BannerListView(LoginRequiredMixin, ListView):

    template_name = "management/banner/list.html"
    queryset = Banner.objects.all()
    paginate_by = 25
    paginator_class = ExtentPaginator

    def get_context_data(self, **kwargs):
        kwargs = super(BannerListView, self).get_context_data(**kwargs)
        show_banners = Show_Banner.objects.all()[0:4]
        kwargs.update(
            {
                'show_banners': show_banners,
            }
        )
        return kwargs


@login_required
@staff_only
def create(request, template='management/banner/create.html'):

    if request.method == "POST":
        _forms = CreateBannerForm(request.POST, request.FILES)
        if _forms.is_valid():
            banner =  _forms.save()
            return HttpResponseRedirect(reverse('management_banner_edit', args=[banner.id]))
    else:
        _forms = CreateBannerForm()

    return render_to_response(
                    template,
                    {
                        'forms': _forms,
                    },
                    context_instance = RequestContext(request) )


@login_required
@staff_only
def edit(request, banner_id, template='management/banner/edit.html'):

    try:
        _banner = Banner.objects.get(pk = banner_id)
    except Banner.DoesNotExist:
        raise Http404

    data = {
        'content_type': _banner.content_type,
        'key': _banner.key,
        'position':_banner.position,
    }

    if request.method == "POST":
        _forms = EditBannerForm(_banner, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
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
