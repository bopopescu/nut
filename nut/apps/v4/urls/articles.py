from django.conf.urls import url, patterns
from apps.v4.views.articles import ArticlesListView, ArticleSearchView

urlpatterns = patterns(
    'apps.v4.views.articles',
    url(r'^$', ArticlesListView.as_view(), name='v4_articles_list'),
    url(r'^search/?$', ArticleSearchView.as_view(), name='v4_articles_search'),
)

__author__ = 'xiejiaxin'
