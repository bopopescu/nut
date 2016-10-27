from django.conf.urls import url, patterns

from apps.top_ad.views.management import TopAdListView, TopAdCreateView, TopAdUpdateView, DisabledTopAdListView

urlpatterns = patterns(
    '',
    url(r'^$', TopAdListView.as_view(), name='manage_topad_list'),
    url(r'^disabled/$', DisabledTopAdListView.as_view(), name='manage_disabled_topad_list'),
    url(r'^new/$', TopAdCreateView.as_view(), name='manage_topad_create'),
    url(r'^(?P<pk>\d+)/update/$', TopAdUpdateView.as_view(), name='manage_topad_update'),
)
