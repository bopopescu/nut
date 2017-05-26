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
from apps.core.models import Entity, Article

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
        abstract = request.data.get('abstract', u'')
        domain = request.data.get('domain', u'1')
        if article_id:
            article = Article.objects.get(pk=article_id)
        elif article_slug:
            article = Article.objects.get(article_slug=article_slug)
        soup = BeautifulSoup(article.content)
        cards = soup.find_all(class_='guoku-card')
        entity_hash_list = [card['data_entity_hash'] for card in cards]
        for index, card in enumerate(cards):
            node = u'<iframe class="spd-faked-goods" data-pos={}></iframe>'.format(index)
            card.replace_with(node)
        goods_info = [{'sku_id': entity_hash, 'tpl_id': 'BdrainrwSpdGoodsHasPic'} for entity_hash in
                      entity_hash_list]
        url = u'http://hoteltest.baidu.com/business/article_publish'
        token = u'spdtkn_test12'

        payload = {
            'app_id': u'1555485749942141',
            'tp_src': u'guocool',
            'v': u'1.0',
            'domain': domain,
            'origin_url': urljoin(u'http://www.guoku.com', article.url).encode('utf-8'),
            'abstract': abstract or article.title,
            'content': unicode(soup),
            'cover_layout': u'one',
            'cover_images': json.dumps([article.cover_url]).encode('utf-8'),
            'service_type': u'1',
            'goods_info': json.dumps(goods_info).encode('utf-8'),
        }
        values = u''.join(payload[key] for key in sorted(payload.iterkeys()))
        values += token
        sign = hashlib.md5(values.encode('utf-8')).hexdigest()
        payload['sign'] = sign
        response = requests.post(url, data=payload)
        return Response(response.json())


upload_article_view = UploadArticleView.as_view()
