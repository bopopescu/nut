from django.conf.urls import url, patterns
from apps.web.views.category import CategoryListView, CategroyGroupListView, OldCategory


urlpatterns = patterns(
    'apps.web.views.category',
    # url(r'^$', 'list', name='web_category_list'),
    url(r'^$', CategoryListView.as_view(), name='web_category_list'),
    url(r'^group/(?P<gid>\d+)/$', CategroyGroupListView.as_view(), name='web_category_group'),
    url(r'^(?P<cid>\d+)/$', 'detail', name='web_category_detail'),
    url(r'^(?P<cid>\d+)/olike/$','detail_like', name='web_category_detail_olike'),
)

__author__ = 'edison7500'
