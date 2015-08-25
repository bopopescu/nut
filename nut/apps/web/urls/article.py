from django.conf.urls import url, patterns

from apps.web.views.article import  SelectionArticleList,\
                                    EditorDraftList,\
                                    EditorArticleCreate,\
                                    EditorArticleEdit,\
                                    ArticleDetail,\
                                    ArticleDelete,\
                                    ArticleRelated,\
                                    NewSelectionArticleList

urlpatterns = patterns(
    'apps.web.views.article',
    url(r'^$', SelectionArticleList.as_view(), name='web_selection_articles'),
    url(r'^list/$', NewSelectionArticleList.as_view(), name='web_selection_articles_new'),

    url(r'^edit/$', EditorDraftList.as_view(), name='web_editor_article_list'),
    url(r'^create/$',EditorArticleCreate.as_view(),name='web_editor_article_create'),
    url(r'^(?P<pk>\d+)/edit/$',EditorArticleEdit.as_view(), name='web_editor_article_edit'),
    url(r'^(?P<pk>\d+)/delete/',ArticleDelete.as_view(),name='web_article_delete'),
    url(r'^(?P<pk>\d+)/',ArticleDetail.as_view(),name='web_article_page'),
    url(r'^(?P<pk>\d+)/related/',ArticleRelated.as_view(),name='web_article_related'),
)

__author__ = 'edison'
