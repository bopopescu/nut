from django.conf.urls import url, patterns

from apps.seller.views.management import SellerCreateView, \
                                         SellerListView, \
                                         SellerUpdateView,\
                                         SellerSectionCreateView,\
                                         SellerSectionUpdateView, \
                                         SellerSectionListView
urlpatterns = patterns(
    '',
    url(r'^/$', SellerListView.as_view() , name='management_seller_list'),
    url(r'^edit/(?P<eid>\d+)/$', SellerUpdateView.as_view() , name='management_seller_update'),
    url(r'^new/$', SellerCreateView.as_view() , name='management_seller_create'),

#     section management

    url(r'^section/edit/(?P<eid>\d+)/$', SellerSectionUpdateView.as_view() , name='management_seller_section_update'),
    url(r'^section/new/$', SellerSectionCreateView.as_view() , name='management_seller_section_create'),
    url(r'^section/$', SellerSectionListView.as_view() , name='management_seller_section_list'),


)