from django.conf.urls import url, patterns

from apps.web.views.article import ArticleList, EditorArticleList, EditorArticleCreate,EditorArticleEdit

urlpatterns = patterns(
    'apps.web.views.article',
    url(r'^list/$', ArticleList.as_view(), name='web_article_list'),
    url(r'^editor/$', EditorArticleList.as_view(), name='web_editor_article_list'),
    url(r'^create/$',EditorArticleCreate.as_view(),name='web_editor_article_create'),
    url(r'^(?P<pk>\d+)/edit/$',EditorArticleEdit.as_view(), name='web_editor_article_edit'),
)

__author__ = 'edison'
