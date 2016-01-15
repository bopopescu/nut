from django.conf.urls import url, patterns
from apps.management.views.statistics import SelectionStatisticsView

urlpatterns = patterns(
    'apps.management.views.statistics',

    url(r'^selection/$', SelectionStatisticsView.as_view(), name='selection_statistics'),
)