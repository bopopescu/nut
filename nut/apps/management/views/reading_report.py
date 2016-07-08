# -*- coding: utf-8 -*-

from django.shortcuts import render
from apps.core.models import Selection_Entity, Entity,Article,Selection_Article
from apps.core.extend.paginator import ExtentPaginator
from django.utils.log import getLogger
from django.views.generic import ListView
from datetime import datetime, timedelta


from haystack.query import SearchQuerySet

log = getLogger('django')

TIME_FORMAT = '%Y-%m-%d 8:00:00'

def readingreport(request):
    model=Selection_Article
    start=(datetime.now()-timedelta(days=150)).strftime(TIME_FORMAT)
    end=datetime.now().strftime(TIME_FORMAT)
    selection_article = Selection_Article.objects.select_related('article').all().filter(article__read_count__gte=1000).filter(create_time__range=(start,end))
    nowtime=datetime.now()
    context={"selection_article":selection_article,"nowtime":nowtime}
    return render(request,'management/reading_report/reading.html',context)





class ReadingReportListView(ListView):
    template_name = 'management/reading_report/reading.html'
    model = Selection_Article
    paginate_by = 40
    context_object_name = 'readingreports'
    paginator_class = ExtentPaginator

    def get_queryset(self):
        start = (datetime.now() - timedelta(days=150)).strftime(TIME_FORMAT)
        end = datetime.now().strftime(TIME_FORMAT)
        queryset = self.model._default_manager.select_related('article').all().filter(article__read_count__gte=1000).filter(create_time__range=(start,end)).order_by("-article__read_count")
        return queryset
'''
    def get_context_data(self, *args, **kwargs):
        start = (datetime.now() - timedelta(days=150)).strftime(TIME_FORMAT)
        end = datetime.now().strftime(TIME_FORMAT)
        context = super(ReadingReportListView, self).get_context_data(*args, **kwargs)
        return context

    def get(self, request, *args, **kwargs):
        readingreports = self.get_queryset()
        self.object_list = readingreports
        context = self.get_context_data()
        return self.render_to_response(context)
'''





