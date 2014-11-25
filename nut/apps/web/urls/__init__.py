from django.conf.urls import url, include, patterns
from apps.web.views.main import AboutView, JobsView, Agreement


urlpatterns = patterns(
    'apps.web.views',

    url(r'^$', 'main.index', name='web_index'),

    url(r'^selection/$', 'main.selection', name='web_selection'),
    url(r'^popular/$', 'main.popular', name='web_popular'),
    url(r'^search/$', 'main.search', name='web_search'),
)

#account
urlpatterns += patterns(
    'apps.web.views.account',
    url(r'^login/$', 'login', name='web_login'),
    url(r'^logout', 'logout', name='web_logout'),
)

# static page
urlpatterns += patterns(
    'apps.web.views.main',

    url(r'^about/$', AboutView.as_view(), name='web_about'),
    url(r'^jobs/$', JobsView.as_view(), name='web_jobs'),
    url(r'^agreement$', Agreement.as_view(), name='web_agreement'),
)


# entity
urlpatterns += patterns(
    'apps.web.views.entity',
    url(r'^entity', include('apps.web.urls.entity')),
)

__author__ = 'edison7500'
