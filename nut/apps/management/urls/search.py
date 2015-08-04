from django.conf.urls import url, patterns
from apps.management.views.search import ManageSearchView


urlpatterns = patterns(
    'apps.management.views.search',
    url(r'^$', ManageSearchView.as_view(), name='management_search'),
)


__author__ = 'xiejiaxin'
