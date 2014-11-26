from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.category',
    url(r'^$', 'list', name='web_category_list'),
    url(r'^(?P<cid>\+d)/$', 'detail', name='web_category_detail'),
)

__author__ = 'edison7500'
