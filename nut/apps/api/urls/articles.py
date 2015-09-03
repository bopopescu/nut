from django.conf.urls import url, patterns

from apps.api.views.articles import RFArticleDetailView, RFArticleListView

urlpatterns = patterns(
    '',
    url(r'^$', RFArticleListView.as_view() , name='restful_article_list'),
    url(r'^(?P<pk>[0-9]+)/$', RFArticleDetailView.as_view() , name='restful_article_detail'),

)