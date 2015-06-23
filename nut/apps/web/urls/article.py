from django.conf.urls import url, patterns

from apps.web.views.article import  SelectionArticleList,\
                                    EditorArticleList,\
                                    EditorArticleCreate,\
                                    EditorArticleEdit,\
                                    ArticleDetail,\
                                    ArticleDelete

urlpatterns = patterns(
    'apps.web.views.article',
    url(r'^$', SelectionArticleList.as_view(), name='web_article_list'),
    url(r'^edit/$', EditorArticleList.as_view(), name='web_editor_article_list'),
    url(r'^create/$',EditorArticleCreate.as_view(),name='web_editor_article_create'),
    url(r'^(?P<pk>\d+)/edit/$',EditorArticleEdit.as_view(), name='web_editor_article_edit'),
    url(r'^(?P<pk>\d+)/delete/',ArticleDelete.as_view(),name='web_article_delete'),
    url(r'^(?P<pk>\d+)/',ArticleDetail.as_view(),name='web_article_page'),
)

__author__ = 'edison'
