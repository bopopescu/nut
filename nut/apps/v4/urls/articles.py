from django.conf.urls import url, patterns
from apps.v4.views.articles import ArticlesListView

urlpatterns = patterns(
    'apps.v4.views.articles',
    url('^$', ArticlesListView.as_view(), name='v4_articles_list'),
)

__author__ = 'xiejiaxin'
