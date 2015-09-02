from django.conf.urls import url, patterns

from apps.api.views.sidebar_banner import RFSidebarBannerListView, RFSidebarBannerDetailView

urlpatterns = patterns(
    '',
    url(r'^$', RFSidebarBannerListView.as_view() , name='restful_sidebar_banner_list'),
    url(r'^(?P<pk>[0-9]+)/$', RFSidebarBannerDetailView.as_view() , name='restful_sidebar_banner_detail'),

)