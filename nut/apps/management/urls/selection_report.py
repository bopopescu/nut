from apps.management.views.selection_report import SelectionReportListView,EntityLikeView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.management.views.selection_report',

    url(r'$', SelectionReportListView.as_view(), name='management_selection_report'),
    #url(r'^entitylike', 'nut.apps.management.views.selection_report.EntityLikeView')
)

