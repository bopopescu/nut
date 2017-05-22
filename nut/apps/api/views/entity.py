# coding=utf-8
from django.utils.log import getLogger
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.api.serializers.entity import EntitySerializer, WebEntitySerializer, SkuSerializer
from apps.core.models import Entity

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
            entity = Entity.objects.get(pk=sku_id)
            serializer = SkuSerializer(entity)
            result['data'] = serializer.data
        except Entity.DoesNotExist:
            result['errno'] = 1
            result['errmsg'] = u'该商品不存在'

        return Response(result)


sku_detail_view = SkuDetailView.as_view()
