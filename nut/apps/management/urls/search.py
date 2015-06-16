from django.conf.urls import url, patterns
from apps.management.views.search import SearchForm


urlpatterns = patterns(
    'apps.management.views.search',
    url(r'^$', SearchForm.as_view(), name='management_search'),
)


__author__ = 'xiejiaxin'
