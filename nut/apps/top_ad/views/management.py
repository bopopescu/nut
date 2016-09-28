# coding=utf-8

from braces.views import StaffuserRequiredMixin

from django.utils.translation import ugettext_lazy as _

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
from django.core.urlresolvers import reverse_lazy

from apps.banners.forms import BaseBannerForm,\
                               BaseBannerCreateForm,\
                               BaseBannerUpdateForm

from apps.core.extend.paginator import ExtentPaginator
from apps.top_ad.models import TopAdBanner





class TopAdCreateForm(BaseBannerCreateForm):
    class Meta:
        model = TopAdBanner
        fields = BaseBannerForm.default_banner_fields + ['display_type', 'content_type']


class TopAdUpdateForm(BaseBannerUpdateForm):
    class Meta:
        model = TopAdBanner
        fields = BaseBannerForm.default_banner_fields + ['display_type', 'content_type']


class TopAdListView(StaffuserRequiredMixin, ListView):
    template_name = 'management/top_ad/list.html'
    paginator_class = ExtentPaginator
    paginate_by = 20
    model = TopAdBanner
    context_object_name = 'banners'

    def get_context_data(self, **kwargs):
        context = super(TopAdBanner, self).get_context_data()
        context['page_title'] = _('Top Ad Banner')
        context['page_sub_title'] = _('Top Ad Banner')
        context['page_crumb_name'] = _("top add")
        context['create_text'] = _('create new')
        return context

    def get_queryset(self):
        return TopAdBanner.objects.active_banners()


class TopAdCreateView(StaffuserRequiredMixin, CreateView):
    form_class = TopAdCreateForm
    model = TopAdBanner
    template_name = 'management/top_ad/create.html'
    success_url = reverse_lazy('manage_topad_list')





