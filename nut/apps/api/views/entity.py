# coding=utf-8
import hashlib
import json
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup
from django.utils.log import getLogger
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.api.serializers.entity import EntitySerializer, WebEntitySerializer, SkuSerializer
from apps.core.models import Entity, Article, PublishBaidu

log = getLogger('django')


class EntityViewSet(ModelViewSet):
    queryset = Entity.objects.filter(status__gt=Entity.remove)
    serializer_class = EntitySerializer


class SelectionViewSet(ModelViewSet):
    queryset = Entity.objects.filter(status=Entity.selection)
    serializer_class = EntitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class WebEntityDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WebEntitySerializer
    queryset = Entity.objects.active()


class SkuDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        result = {
            'errno': 0,
            'errmsg': '',
            'data': {}
        }
        if request.method == 'GET':
            sku_id = request.query_params.get('sku_id', '')
        elif request.method == 'POST':
            sku_id = request.data.get('sku_id', '')
        else:
            # 不支持的方式
            result['errno'] = 1
            result['errmsg'] = u'不支持的方法'
            return Response(result)

        try:
            entity = Entity.objects.get(entity_hash=sku_id)
            serializer = SkuSerializer(entity)
            result['data'] = serializer.data
        except Entity.DoesNotExist:
            result['errno'] = 1
            result['errmsg'] = u'该商品不存在'

        return Response(result)


sku_detail_view = SkuDetailView.as_view()


class UploadArticleView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        article_id = request.data.get('article_id')
        article_slug = request.data.get('article_slug', '')
        article_url = request.data.get('article_url', '')
        abstract = request.data.get('abstract', u'')
        title = request.data.get('title', u'')
        domain = request.data.get('domain', u'1')

        try:
            if article_id:
                article = Article.objects.get(pk=article_id)
            elif article_slug:
                article = Article.objects.get(article_slug=article_slug)
            elif article_url:
                article_slug = article_url.split('/')[-2]
                article = Article.objects.get(article_slug=article_slug)
            else:
                return Response(u'article_id、article_slug、article_url至少包含一个')
        except Article.DoesNotExist:
            return Response(u'文章不存在。 ({})'.format(article_id or article_slug or article_url))

        soup = BeautifulSoup(article.content)
        cards = soup.find_all(class_='guoku-card')
        entity_hash_list = [card['data_entity_hash'] for card in cards]
        for index, card in enumerate(cards):
            new_tag = soup.new_tag(u'iframe')
            new_tag['class'] = 'spd-faked-goods'
            new_tag['data-pos'] = index
            card.replace_with(new_tag)
        goods_info = [{'sku_id': entity_hash, 'tpl_id': 'BdrainrwSpdGoodsHasPic'} for entity_hash in
                      entity_hash_list]
        url = u'http://sfc.baidu.com/business/article_publish'
        token = u'4484c8afa31b315ec3f21e7989e35464'

        content = unicode(soup).replace('\n', '')

        payload = {
            'app_id': u'1555485749942141',
            'tp_src': u'guocool',
            'v': u'1.0',
            'domain': domain,
            'origin_url': urljoin(u'http://www.guoku.com', article.url).encode('utf-8'),
            'title': title or article.title,
            'abstract': abstract or '',
            'content': content,
            'cover_layout': u'one',
            'cover_images': json.dumps([article.cover_url]).encode('utf-8'),
            'service_type': u'1',
            'goods_info': json.dumps(goods_info).encode('utf-8'),
        }
        values = u''.join(payload[key] for key in sorted(payload.iterkeys()))
        values += token
        sign = hashlib.md5(values.encode('utf-8')).hexdigest()
        payload['sign'] = sign

        try:
            response = requests.post(url, data=payload)
            return Response(response.text)
        except Exception as e:
            return Response(unicode(e))


upload_article_view = UploadArticleView.as_view()


class PublishBaiduView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        article_url = request.data.get('article_url', '')
        abstract = request.data.get('abstract', u'')
        title = request.data.get('title', u'')
        domain = request.data.get('domain', u'1')
        cover_images = request.data.get('cover_images', u'')

        article_slug = article_url.split('/')[-2]
        article = Article.objects.get(article_slug=article_slug)

        try:
            PublishBaidu.objects.create(title=title, abstract=abstract, article_id=article.id, domain=domain, cover_images=cover_images)
            return Response({'code': 0, 'message': '创建成功'})
        except Exception as e:
            return Response(unicode(e))

create_publish_baidu_view = PublishBaiduView.as_view()
