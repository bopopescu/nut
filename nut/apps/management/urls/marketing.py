from django.conf.urls import url, patterns
from apps.management.views.marketing import LaunchBoardListView, NewLaunchBoardView, EditLaunchBoardView

urlpatterns = patterns(
    'apps.management.views.marketing',
    url(r'^$', LaunchBoardListView.as_view(), name='management_marketing'),
    url(r'^create/$', NewLaunchBoardView.as_view(), name='management_create_launch_image'),
    url(r'^(?P<pk>\d+)/edit/$', EditLaunchBoardView.as_view(), name='management_edit_launch_image'),
)