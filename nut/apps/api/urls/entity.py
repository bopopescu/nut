# coding=utf-8
from django.conf.urls import url, patterns
from apps.api.views.entity import WebEntityDetailView, sku_detail_view, upload_article_view, create_publish_baidu_view

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>[0-9]+)/$', WebEntityDetailView.as_view(), name='restful_web_entity_detail'),
    url(r'entity-sku-detail', sku_detail_view, name='sku_detail_view'),
    url(r'upload-article', upload_article_view),
    url(r'create-publish-baidu', create_publish_baidu_view),
)
