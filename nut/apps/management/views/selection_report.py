# -*- coding: utf-8 -*-


from apps.core.models import Selection_Entity
from apps.core.extend.paginator import ExtentPaginator
from django.utils.log import getLogger
from django.views.generic import ListView
from datetime import datetime, timedelta

log = getLogger('django')

TIME_FORMAT = '%Y-%m-%d 8:00:00'

def get_time_range():
    if datetime.now().hour > 8:
        today_start = datetime.now().strftime(TIME_FORMAT)
        today_end = (datetime.now() + timedelta(days=1)).strftime(TIME_FORMAT)
    else:
        today_start = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
        today_end = datetime.now().strftime(TIME_FORMAT)

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
        self.status =  self.request.GET.get('status', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get("end_date")
        if start_date == 'lastweek':
            self.start_time = start_date
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=7)).strftime(TIME_FORMAT)), (datetime.now()+timedelta(days=1)).strftime(TIME_FORMAT)
        elif start_date == 'lastmonth':
            self.start_time = start_date
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=30)).strftime(TIME_FORMAT)),(datetime.now()+timedelta(days=1)).strftime(TIME_FORMAT)
        elif start_date and end_date:
            self.start_time = None
            self.start_date, self.end_date = start_date, end_date
        else:
            self.start_time = 'yesterday'
            self.start_date, self.end_date = get_time_range()
        queryset = Selection_Entity.objects.filter(pub_time__range=(self.start_date, self.end_date))
        selections = self.status_filter(self.status, queryset)
        return selections

    def status_filter(self, status, queryset):
        if status == '1':
            entity_list = self.get_most_click(queryset)
        elif status == '2':
            entity_list = self.get_sold(queryset)
        else:
            entity_list = self.get_like_best(queryset)
        return  entity_list

    def get_like_best(self, queryset):
        like_best = filter(lambda x: x.entity.like_count>100, queryset)
        return like_best

    def get_sold(self, queryset):  #Todo
        return queryset

    def get_most_click(self, queryset):   #Todo
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(SelectionReportListView, self).get_context_data(*args, **kwargs)
        context['status'] =  self.status
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['start_time'] = self.start_time
        return context

    def get(self, request, *args, **kwargs):

        selections = self.get_queryset()
        self.object_list = selections
        context = self.get_context_data()
        return self.render_to_response(context)






