# coding=utf-8

from braces.views import StaffuserRequiredMixin

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
from django.core.urlresolvers import reverse_lazy

from apps.banners.forms import BaseBannerForm,\
                               BaseBannerCreateForm,\
                               BaseBannerUpdateForm

from apps.core.extend.paginator import ExtentPaginator
from apps.top_ad.models import TopAdBanner


class TopAdCreateForm(BaseBannerCreateForm):
    applink = forms.CharField(label='Link',
                              help_text='''
                                        for entity ,user: fill in entity id , user id.
                               ''')

    class Meta:
        model = TopAdBanner
        fields = ['display_type', 'content_type', 'applink', 'img_file', 'status']


class TopAdUpdateForm(BaseBannerUpdateForm):
    applink = forms.CharField(label='Link',
                              help_text='''
                                        for entity ,user: fill in entity id , user id.
                               ''')

    class Meta:
        model = TopAdBanner
        fields = ['display_type', 'content_type', 'applink', 'img_file', 'status']


class TopAdListView(StaffuserRequiredMixin, ListView):
    template_name = 'management/top_ad/list.html'
    paginator_class = ExtentPaginator
    paginate_by = 20
    model = TopAdBanner
    context_object_name = 'banners'

    def get_context_data(self, **kwargs):
        context = super(TopAdListView, self).get_context_data()
        context['page_title'] = _('Top Ad Banner')
        context['page_sub_title'] = _('Top Ad Banner')
        context['page_crumb_name'] = _("top add")
        context['create_text'] = _('create new')
        return context

    def get_queryset(self):
        return TopAdBanner.objects.active_banners()


class DisabledTopAdListView(TopAdListView):
    def get_queryset(self):
        return TopAdBanner.objects.disabled_banners()


class TopAdCreateView(StaffuserRequiredMixin, CreateView):
    form_class = TopAdCreateForm
    model = TopAdBanner
    template_name = 'management/top_ad/create.html'
    success_url = reverse_lazy('manage_topad_list')


class TopAdUpdateView(StaffuserRequiredMixin, UpdateView):
    form_class = TopAdUpdateForm
    model = TopAdBanner
    template_name = 'management/top_ad/update.html'
    success_url = reverse_lazy('manage_topad_list')
