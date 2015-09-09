from django.conf.urls import url, patterns

from apps.api.views.sla import RFSlaListView, RFSlaDetailView

urlpatterns = patterns(
    '',
    url(r'^$', RFSlaListView.as_view() , name='restful_sla_list'),
    url(r'^(?P<pk>[0-9]+)/$', RFSlaDetailView.as_view() , name='restful_sla_detail'),

)