from apps.management.views.reading_report import ReadingReportListView
from django.conf.urls import url, patterns
# from . import reading_report

urlpatterns = patterns(
    'apps.management.views.reading_report',
    url(r'$', 'readingreport', name='management_reading_report'),
)

