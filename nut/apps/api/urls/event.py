from django.conf.urls import url, patterns
from apps.api.views.events import RFEventListView, RFEventDetailView

urlpatterns = patterns(
    '',

    url(r'^$', RFEventListView.as_view(), name='restful_event_list' ),
    url(r'^(?P<pk>[0-9]+)/$', RFEventDetailView.as_view(), name='restful_event_detail' ),
    # url(r'^(?P<event_id>[0-9]+)/articles', )
)