from apps.management.views.editor_report import EditorReportListView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.management.views.editor_report',

    url(r'$', EditorReportListView.as_view(), name='management_editor_report'),

)

