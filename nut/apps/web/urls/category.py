from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.category',
    url(r'^$', 'list', name='web_category_list'),
)

__author__ = 'edison7500'
