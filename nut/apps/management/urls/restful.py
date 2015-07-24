from django.conf.urls import url, patterns

from apps.management.views.users import RESTfulUserListView
from apps.management.views.article import RESTfulArticleListView, RESTfulArticleDetail

urlpatterns = patterns(
   '',
    # disabled by AnChen, to be continued
    # url(r'^users/$', RESTfulUserListView.as_view() , name='restful_user_list'),
    # url(r'^articles/$', RESTfulArticleListView.as_view() , name='restful_article_list'),
    # url(r'^articles/(?P<pk>\d+)/$', RESTfulArticleDetail.as_view() , name='restful_article_detail'),

)