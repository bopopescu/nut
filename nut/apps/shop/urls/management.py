from django.conf.urls import url, patterns

from apps.shop.views.management import StoreBannerCreateView,\
                                       StoreBannerListView,\
                                       StoreBannerDeleteView,\
                                       StoreBannerUpdateView

urlpatterns = patterns(
    '',
    url(r'^banners/$', StoreBannerListView.as_view(), name='manage_store_banners' ),
    url(r'^banners/new/$', StoreBannerCreateView.as_view(),name='manage_store_banners_create' ),
    url(r'^banners/(?P<pk>\d+)/update/$', StoreBannerUpdateView.as_view(), name='manage_store_banners_update' ),
    url(r'^banners/(?P<pk>\d+)/delete/$', StoreBannerDeleteView.as_view(), name='manage_store_banners_delete' ),
)