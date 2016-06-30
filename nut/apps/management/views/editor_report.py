# -*- coding: utf-8 -*-


from apps.core.models import  GKUser
from apps.core.extend.paginator import ExtentPaginator
from django.utils.log import getLogger
from django.views.generic import ListView
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from braces.views import UserPassesTestMixin

log = getLogger('django')

TIME_FORMAT = '%Y-%m-%d 8:00:00'


class EditorReportListView(UserPassesTestMixin,  ListView):

    def test_func(self, user):
        return user.is_admin

    template_name = 'management/editor_report/list.html'
    model = GKUser
    paginate_by = 40
    context_object_name = 'editors'
    paginator_class = ExtentPaginator


    def get_queryset(self):
        self.status =  self.request.GET.get('status', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get("end_date")
        if start_date == 'lastmonth':
            self.start_time = start_date
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=30)).strftime(TIME_FORMAT)),(datetime.now()+timedelta(days=1)).strftime(TIME_FORMAT)
        elif start_date and end_date:
            self.start_time = None
            self.start_date, self.end_date = start_date, end_date
        else:
            self.start_time = 'lastweek'
            self.start_date, self.end_date = ((datetime.now() - timedelta(days=7)).strftime(TIME_FORMAT)), (
                datetime.now() + timedelta(days=1)).strftime(TIME_FORMAT)
        editors = GKUser.objects.editor()
        for editor in editors:
            editor.report = {}
            entities = editor.entities.filter(created_time__range=(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S'),
                                              datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')))
            editor.report['entity_count'] = entities.count()
            editor.report['entity_like_count'] = entities.aggregate(Count('likes')).get('likes__count') or 0
            articles = editor.articles.filter(created_datetime__range=(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S'),
                                              datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')))
            editor.report['article_count'] = articles.count()
            editor.report['article_read_count'] = articles.aggregate(Sum('read_count')).get('read_count__sum', 0) or 0
            editor.report['article_dig_count'] = articles.aggregate(Count('digs')).get('digs__count') or 0

        return editors

    def get_context_data(self, *args, **kwargs):

        context = super(EditorReportListView, self).get_context_data(*args, **kwargs)
        context['status'] =  self.status
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['start_time'] = self.start_time
        return context

    def get(self, request, *args, **kwargs):

        editors = self.get_queryset()
        self.object_list = editors
        context = self.get_context_data()
        return self.render_to_response(context)