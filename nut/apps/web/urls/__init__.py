from django.conf.urls import url, include, patterns

urlpatterns = patterns(
    'apps.web.views',

    url(r'^$', 'main.index', name='web_index'),

    url(r'^selection/$', 'main.selection', name='web_selection'),
    url(r'^popular/$', 'main.popular', name='web_popular'),
)

__author__ = 'edison7500'
