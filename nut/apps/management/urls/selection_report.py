from apps.management.views.selection_report import SelectionReportListView
from django.conf.urls import url, patterns
from django.views.generic import RedirectView


urlpatterns = patterns(
    'apps.management.views.selection_report',

    url(r'$', SelectionReportListView.as_view(), name='management_selection_report'),

)

