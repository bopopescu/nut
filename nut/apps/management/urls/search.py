from django.conf.urls import url, patterns
from apps.management.views.search import ManageSearchView, AutoCompleteView


urlpatterns = patterns(
    'apps.management.views.search',
    url(r'^$', ManageSearchView.as_view(), name='management_search'),
    url(r'^autocomplete/$', AutoCompleteView.as_view(), name='management_autocomplete'),
)


__author__ = 'xiejiaxin'
