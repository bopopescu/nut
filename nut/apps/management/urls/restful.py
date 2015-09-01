from django.conf.urls import url, patterns
from rest_framework.urlpatterns import format_suffix_patterns


from apps.management.views.users import RESTfulUserListView
from apps.management.views.article import RESTfulArticleListView, RESTfulArticleDetail


from apps.management.views.restful import SbbannerAppView

from apps.management.views.sidebar_banner import RFSidebarBannerListView, RFSidebarBannerDetailView

urlpatterns = patterns(
    '',
    url(r'^sbbanners/$', RFSidebarBannerListView.as_view() , name='restful_sidebar_banner_list'),
    url(r'^sbbanners/(?P<pk>[0-9]+)/$', RFSidebarBannerDetailView.as_view() , name='restful_sidebar_banner_detail'),


    url(r'^application/sbbanner/$', SbbannerAppView.as_view() , name='restful_app_sbbanner'),


    # disabled by AnChen, to be continued
    # url(r'^users/$', RESTfulUserListView.as_view() , name='restful_user_list'),
    # url(r'^articles/$', RESTfulArticleListView.as_view() , name='restful_article_list'),
    # url(r'^articles/(?P<pk>\d+)/$', RESTfulArticleDetail.as_view() , name='restful_article_detail'),

)
