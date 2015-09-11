from django.conf.urls import url, patterns

from apps.api.views.friendly_link import RFFriendlyLinkListView, RFFriendlyLinkDetailView


urlpatterns = patterns(
    '',
    url(r'^$', RFFriendlyLinkListView.as_view() , name='restful_friendly_link_list'),
    url(r'^(?P<pk>[0-9]+)/$', RFFriendlyLinkDetailView.as_view() , name='restful_friendly_link_detail'),
)