from django.conf.urls import url, patterns
from apps.web.views.category import CategoryGroupListView
from apps.web.views.category import CategoryDetailView
from apps.web.views.category import CategoryListView


urlpatterns = patterns(
    'apps.web.views.category',
    url(r'^$', CategoryListView.as_view(), name='web_category_list'),
    url(r'^group/(?P<gid>\d+)/$', CategoryGroupListView.as_view(), name='web_category_group'),
    url(r'^(?P<cid>\d+)/$', CategoryDetailView.as_view(), name='web_category_detail'),
    url(r'^(?P<cid>\d+)/olike/$','detail_like', name='web_category_detail_olike'),
)

__author__ = 'edison7500'
