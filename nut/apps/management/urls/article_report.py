from apps.management.views.article_report import ArticleReportListView
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.management.views.article_report',

    url(r'$', ArticleReportListView.as_view(), name='management_article_report'),

)

