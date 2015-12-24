from django.conf.urls import url, patterns
from apps.management.views.recommendation import RecommendListView


urlpatterns = patterns(
    'apps.management.views.recommendation',
    # url(r'^$', 'list', name='management_recommend_banner'),
    url(r'^$', RecommendListView.as_view(), name='management_recommend_banner'),
    url(r'^(?P<rid>\d+)/$', 'show_list', name='management_event_show_recommendation'),
    url(r'^create/$', 'create', name='management_recommend_create'),
    url(r'^create/(?P<event_id>\d+)/$', 'create', name='management_recommend_create'),
    url(r'^(?P<event_banner_id>\d+)/edit/$', 'edit', name='management_recommend_edit'),
)

__author__ = 'edison'
