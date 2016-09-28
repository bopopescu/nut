from django.conf.urls import url, patterns

from apps.top_ad.views.management import TopAdListView, TopAdCreateView

urlpatterns = patterns(
    '',
    url(r'^$', TopAdListView.as_view(), name='manage_topad_list'),
    url(r'^new/$', TopAdCreateView.as_view(), name='manage_topad_create'),
)
