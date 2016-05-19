# -*- coding: utf-8 -*-


from apps.core.models import Selection_Entity
from apps.core.extend.paginator import ExtentPaginator

from django.utils.log import getLogger
from django.views.generic import ListView
from datetime import datetime, timedelta

log = getLogger('django')

def get_time_range():
    if datetime.now().hour > 8:
        today_start = datetime.now().strftime('%Y-%m-%d 8:00:00')
        today_end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 8:00:00')
    else:
        today_start = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 8:00:00')
        today_end = datetime.now().strftime('%Y-%m-%d 8:00:00')

    return today_start, today_end

def get_today_Secelction():
    return Selection_Entity.objects.filter(pub_time__range=(get_time_range()))


class SelectionReportListView(ListView):
    template_name = 'management/selection_report/list.html'
    model = Selection_Entity
    paginate_by = 10
    context_object_name = 'selections'
    paginator_class = ExtentPaginator



    def get_queryset(self):
        # qs = super(SelectionReportListView,self).get_queryset()
        status =  self.request.GET.get('status', None)
        today_selection = Selection_Entity.objects.filter(pub_time__range=(get_time_range()))
        if status is None or status == '0':
            entity_list = self.get_like_best(today_selection)
        elif status == '1':
            entity_list = self.get_most_click(today_selection)
        elif status == '2':
            entity_list = self.get_sold(today_selection)

        return  entity_list

    def get_like_best(self, today_selection):
        like_best = filter(lambda x: x.entity.like_count>10, today_selection)
        return like_best

    def get_sold(self, queryset):
        pass

    def get_most_click(self, queryset):
        pass


    def get_context_data(self, *args, **kwargs):
        context = super(SelectionReportListView, self).get_context_data(*args, **kwargs)
        context['status'] =  self.request.GET.get('status', None)
        return context




