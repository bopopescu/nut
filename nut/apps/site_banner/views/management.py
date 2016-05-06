# coding=utf-8

from apps.site_banner.models import SiteBanner
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from apps.core.extend.paginator import ExtentPaginator
from braces.views import AjaxResponseMixin, JSONResponseMixin
import json

from django.core.urlresolvers import reverse_lazy
from apps.banners.forms import BaseBannerForm,\
                               BaseBannerCreateForm,\
                               BaseBannerUpdateForm

from braces.views import StaffuserRequiredMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin


class SiteBannerCreateForm(BaseBannerCreateForm):
    class Meta:
        model = SiteBanner
        fields = BaseBannerForm.sitebanner_default_fields + ['active_status', 'banner_title', 'banner_desc',
                                                        'content_type', 'app_show_status','web_mainpage_show_status',
                                                        'web_sidebar_show_status',
                                                         ]

class SiteBannerUpdateForm(BaseBannerUpdateForm):
    class Meta:
        model = SiteBanner
        fields = BaseBannerForm.sitebanner_default_fields + ['active_status', 'banner_title', 'banner_desc',
                                                         'content_type', 'app_show_status','web_mainpage_show_status',
                                                         'web_sidebar_show_status',
                                                         ]


class SiteBannerCreateView(StaffuserRequiredMixin,CreateView):
    form_class = SiteBannerCreateForm
    model = SiteBanner
    template_name = 'management/site_banner_create.html'
    success_url = reverse_lazy('manage_sitebanners')

class SiteBannerUpdateView(StaffuserRequiredMixin, UpdateView):
    form_class  = SiteBannerUpdateForm
    model = SiteBanner
    template_name = 'management/site_banner_edit.html'
    success_url = reverse_lazy('manage_sitebanners')

class SiteBannerDeleteView(StaffuserRequiredMixin,DeleteView):
    model = SiteBanner
    template_name = 'management/site_banner_delete.html'
    success_url = reverse_lazy('manage_sitebanners')

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
                'msg': 'can not get remove id list json string'
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
    template_name = 'management/site_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  SiteBanner
    context_object_name = 'banners'
    def get_queryset(self):

        return SiteBanner.objects.get_active_banner().order_by('-app_show_status', '-web_mainpage_show_status',
                                                 '-web_sidebar_show_status', 'position')

    def get(self, request, *args, **kwargs):
        #
        # TODO : EXPLAIN  WHY USE COOKIE ?
        #  1.       USE querystring to persist state, do not use cookie

        cookie_checked = request.COOKIES.get('checked')
        if cookie_checked is None:    #无cookie 首次访问
            checked = ['0', '1', '2']
        else:
            checked = request.GET.getlist('checks[]')
            if not checked and request.GET.get('page'):       # 有cookie checked为空 翻页的情况
                checked = cookie_checked.split('|')
            elif request.GET.get('from') or cookie_checked == '-1' and len(checked) == 0: #cookie为-1 checked为空
                checked = ['0', '1', '2']
            else:                 # 有cookie 有checked 修改勾选的情况
                checked = checked

        queryset = get_select(checked)
        self.object_list = queryset
        context = self.get_context_data()
        context['checked'] = checked
        response = self.render_to_response(context)
        if isinstance(checked, list):
            if len(checked) == 0:
                cookie_checked = '-1'           # 勾选为空
            else:
                cookie_checked = '|'.join(checked)
        response.set_cookie('checked', cookie_checked)
        return response

def get_select(checked):
    # 如果多一个 CHECK 怎么办?


    # TODO  : REFACTTOR HERE
    # 1. SHOULD NOT USE MAGIC NUMBER
    # 2. LOGIC IS NOT CLEAR

    if len(checked) == 0:
        return SiteBanner.objects.get_active_banner().filter(app_show_status=False, web_mainpage_show_status=False,
                                                             web_sidebar_show_status=False)
    elif len(checked) == 1:
        if checked[0] == '' or int(checked[0]) == -1:
            return SiteBanner.objects.get_active_banner().filter(app_show_status=False, web_mainpage_show_status=False,
                                                             web_sidebar_show_status=False)
        elif int(checked[0]) == 0:
            return SiteBanner.objects.get_active_banner().filter(app_show_status=True)
        elif int(checked[0]) == 1:
            return SiteBanner.objects.get_active_banner().filter(web_mainpage_show_status=True)
        else:
            return SiteBanner.objects.get_active_banner().filter(web_sidebar_show_status=True)
    elif len(checked) == 2:

        if not '0'  in checked:
            return SiteBanner.objects.get_active_banner().filter(Q(web_mainpage_show_status=True) | Q(web_sidebar_show_status=True))
        elif not '1' in checked:
            return SiteBanner.objects.get_active_banner().filter(Q(app_show_status=True) | Q(web_sidebar_show_status=True))
        else:
            return SiteBanner.objects.get_active_banner().filter(Q(app_show_status=True) | Q(web_mainpage_show_status=True))
    else:
        return SiteBanner.objects.get_active_banner().filter(Q(app_show_status=True) | Q(web_mainpage_show_status=True) |
                                                      Q(web_sidebar_show_status=True))


class SiteBannerInactiveListView(StaffuserRequiredMixin,ListView):
    template_name = 'management/site_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  SiteBanner
    context_object_name = 'banners'
    def get_queryset(self):
        return SiteBanner.objects.get_inactive_banner()