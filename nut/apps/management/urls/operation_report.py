from apps.management.views.operation_report import OperationReportListView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.management.views.operation_report',

    url(r'$', OperationReportListView.as_view(), name='management_operation_report'),

)

