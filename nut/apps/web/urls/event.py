from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.event',
    url(r'^$', 'home', name='web_event_home'),
    url(r'^(?P<slug>\d+)/$', 'event', name='web_event'),
    url(r'^list/$', 'elist', name='web_event_list'),
)
