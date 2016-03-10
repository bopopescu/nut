from django.conf.urls import url, patterns

from apps.shop.views.management import StoreBannerCreateView,\
                                       StoreBannerListView,\
                                       StoreBannerDeleteView,\
                                       StoreBannerUpdateView,\
                                       StoreRecommendListView,\
                                       StoreRecommendCreateView,\
                                       StoreRecommendUpdateView,\
                                       StoreRecommendDeleteView


urlpatterns = patterns(
    '',
    url(r'^banners/$', StoreBannerListView.as_view(), \
                       name='manage_store_banners' ),
    url(r'^banners/new/$', StoreBannerCreateView.as_view(),\
                       name='manage_store_banners_create' ),
    url(r'^banners/(?P<pk>\d+)/update/$', StoreBannerUpdateView.as_view(),\
                       name='manage_store_banners_update' ),
    url(r'^banners/(?P<pk>\d+)/delete/$', StoreBannerDeleteView.as_view(),\
                       name='manage_store_banners_delete' ),


     url(r'^recommend/$', StoreRecommendListView.as_view(), \
                       name='manage_store_recommends' ),
    url(r'^recommend/new/$', StoreRecommendCreateView.as_view(),\
                       name='manage_store_recommends_create' ),
    url(r'^recommend/(?P<pk>\d+)/update/$', StoreRecommendUpdateView.as_view(),\
                       name='manage_store_recommends_update' ),
    url(r'^recommend/(?P<pk>\d+)/delete/$', StoreRecommendDeleteView.as_view(),\
                       name='manage_store_recommends_delete' ),
)