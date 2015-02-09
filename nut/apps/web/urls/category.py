from django.conf.urls import url, patterns
from apps.web.views.category import CategoryListView, CategroyGroupListView


urlpatterns = patterns(
    'apps.web.views.category',
    # url(r'^$', 'list', name='web_category_list'),
    url(r'^$', CategoryListView.as_view(), name='web_category_list'),
    url(r'^group/(?P<cid>\d+)/$', CategroyGroupListView.as_view(), name='web_category_group'),
    url(r'^(?P<cid>\d+)/$', 'detail', name='web_category_detail'),
)

__author__ = 'edison7500'
