from django.conf.urls import url, include, patterns
from apps.web.views.main import AboutView, JobsView, Agreement


urlpatterns = patterns(
    'apps.web.views',

    url(r'^$', 'main.index', name='web_index'),

    url(r'^selection/$', 'main.selection', name='web_selection'),
    url(r'^popular/$', 'main.popular', name='web_popular'),
    url(r'^search/$', 'main.search', name='web_search'),
)


# static page
urlpatterns += patterns(
    'apps.web.views.main',

    url(r'^about/$', AboutView.as_view(), name='web_about'),
    url(r'^jobs/$', JobsView.as_view(), name='web_jobs'),
    url(r'^agreement$', Agreement.as_view(), name='web_agreement'),
)

__author__ = 'edison7500'
