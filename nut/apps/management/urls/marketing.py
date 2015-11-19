from django.conf.urls import url, patterns
from apps.management.views.marketing import LaunchBoardListView

urlpatterns = patterns(
    'apps.management.views.marketing',
    url('^$', LaunchBoardListView.as_view(), name='management_marketing'),
)