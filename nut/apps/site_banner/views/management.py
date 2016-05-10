# coding=utf-8


from urlparse import urlparse, parse_qs
from apps.site_banner.models import SiteBanner
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from apps.core.extend.paginator import ExtentPaginator
from braces.views import AjaxResponseMixin, JSONResponseMixin
import json
from apps.management.decorators import staff_only
from django.core.urlresolvers import reverse_lazy
from apps.banners.forms import BaseBannerForm,\
                               BaseBannerCreateForm,\
                               BaseBannerUpdateForm

from braces.views import StaffuserRequiredMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin


class SiteBannerCreateForm(BaseBannerCreateForm):
    class Meta:
        model = SiteBanner
        fields = ['link', 'applink', 'content_type', 'position', 'img_file', 'active_status', 'banner_title',
                                                'banner_desc','app_show_status','web_mainpage_show_status',
                                                'web_sidebar_show_status']

class SiteBannerUpdateForm(BaseBannerUpdateForm):
    class Meta:
        model = SiteBanner
        fields = ['link', 'applink', 'content_type', 'position', 'img_file', 'active_status', 'banner_title',
                                                'banner_desc','app_show_status','web_mainpage_show_status',
                                                'web_sidebar_show_status']


class SiteBannerCreateView(StaffuserRequiredMixin,CreateView):
    form_class = SiteBannerCreateForm
    model = SiteBanner
    template_name = 'management/management_sitebanner/site_banner_create.html'
    success_url = '/management/sitebanner/banners/?from=create'

class SiteBannerUpdateView(StaffuserRequiredMixin, UpdateView):
    form_class  = SiteBannerUpdateForm
    model = SiteBanner
    template_name = 'management/management_sitebanner/site_banner_edit.html'
    success_url = '/management/sitebanner/banners/?from=update'

class SiteBannerDeleteView(StaffuserRequiredMixin,DeleteView):
    model = SiteBanner
    template_name = 'management/management_sitebanner/site_banner_delete.html'
    success_url = '/management/sitebanner/banners/?from=delete'
    def delete(self, request, *args, **kwargs):
        '''override delete method, dont't actually delete the object, just
            set the active_status to false'''

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.active_status = False
        self.object.save()
        return HttpResponseRedirect(success_url)

class SiteBannerSaveView(StaffuserRequiredMixin, AjaxResponseMixin, JSONResponseMixin, View):
    model = SiteBanner

    def save_update(self, id_list):
        app_id_list = id_list[0]
        mainpage_id_list = id_list[1]
        sidebar_id_list = id_list[2]
        obj_ids = id_list[3]
        positions = id_list[4]

        for (id, p) in zip(obj_ids, positions):
            banner = SiteBanner.objects.get(id=id)
            banner.position = int(p)
            banner.save()
            if str(id) in app_id_list:
                banner.app_show_status = True
                banner.save()
            else:
                banner.app_show_status = False
                banner.save()
            if str(id) in mainpage_id_list:
                banner.web_mainpage_show_status = True
                banner.save()
            else:
                banner.web_mainpage_show_status = False
                banner.save()
            if str(id) in sidebar_id_list:
                banner.web_sidebar_show_status = True
                banner.save()
            else:
                banner.web_sidebar_show_status = False
                banner.save()

        return

    def post_ajax(self, request, *args, **kwargs):
        id_list_jsonstring = request.POST.get('id_list', None)
        if not id_list_jsonstring:
            res = {
                'error': 1,
                'msg': 'can not get  id list json string'
            }
            return self.render_json_response(res)
        id_list = json.loads(id_list_jsonstring)

        if id_list[0] or id_list[1] or id_list[2]:
            try:
                self.save_update(id_list)
            except Exception as e:
                res = {
                    'error': 1,
                    'msg': 'error %s' % e.message
                }
                return self.render_json_response(res)
            res = {
                'error': 0,
                'msg': 'Save Update Success'
            }
            return self.render_json_response(res)
        else:
            res = {
                'error': 1,
                'msg': 'Save Update Failed'
            }
            return self.render_json_response(res)

class SiteBannerActiveListView(StaffuserRequiredMixin, AjaxResponseMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin,  View):
    template_name = 'management/management_sitebanner/site_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  SiteBanner
    context_object_name = 'banners'
    def get_queryset(self):

        return SiteBanner.objects.get_active_banner().order_by('-app_show_status', '-web_mainpage_show_status',
                                                 '-web_sidebar_show_status', 'position')


    def get(self, request, *args, **kwargs):
        come_from = request.GET.get('from')
        if come_from:
            checked = ['app_show_status', 'web_mainpage_show_status', 'web_sidebar_show_status']
        else:
            checked = request.GET.getlist('checks')

        queryset = get_select(checked)
        self.object_list = queryset
        context = self.get_context_data()
        context['checks'] = '&checks='.join(checked)

        return self.render_to_response(context)

def get_select(checked):

    # TODO  : REFACTTOR HERE
    # 1. SHOULD NOT USE MAGIC NUMBER
    # 2. LOGIC IS NOT CLEAR
    if len(checked) == 0 or checked[0] == '':
        return SiteBanner.objects.get_active_banner().filter(app_show_status=False, web_mainpage_show_status=False,
                                                  web_sidebar_show_status=False)
    # ALWASY NONE ???
    fiter_condition = None
    for select_field in checked:
        q = Q(**{select_field: True})

        if fiter_condition: #ALWAYS NONE ?
            fiter_condition = fiter_condition | q  # or & for filtering
        else:
            fiter_condition = q

    result = SiteBanner.objects.get_active_banner().filter(fiter_condition)
    return result

class SiteBannerInactiveListView(StaffuserRequiredMixin,ListView):
    template_name = 'management/management_sitebanner/site_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  SiteBanner
    context_object_name = 'banners'
    def get_queryset(self):
        return SiteBanner.objects.get_inactive_banner()