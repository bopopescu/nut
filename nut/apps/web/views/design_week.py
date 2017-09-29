# encoding: utf-8
from django.http import HttpResponseRedirect
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.pagination import BasePaginationSerializer
from rest_framework.response import Response

from apps.core.models import GKUser, Entity
from apps.shop.models import Shop


class DesignWeekSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='design_week_url', read_only=True)
    liked = serializers.IntegerField(source='like_count', read_only=True)
    image = serializers.CharField(source='chief_image', read_only=True)
    price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Entity
        fields = ('title', 'price', 'image', 'url', 'liked')


class DesignWeekViewSet(viewsets.ReadOnlyModelViewSet):
    def __init__(self, *args, **kwargs):
        super(DesignWeekViewSet, self).__init__(**kwargs)
        self.permission_classes = ()
        self.page_kwarg = 'page_offset'
        self.paginate_by_param = 'page_size'
        self.serializer_class = DesignWeekSerializer
        self.queryset = self.get_queryset()

    def list(self, request, *args, **kwargs):
        if request.query_params == {}:
            return HttpResponseRedirect(request.path + "?page_size=30&page_offset=1")
        instance = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return get_auth_seller_entities()

    def get_pagination_serializer(self, page):
        class SerializerClass(NewPaginationSerializer):
            class Meta:
                object_serializer_class = self.get_serializer_class()

        pagination_serializer_class = SerializerClass
        context = self.get_serializer_context()
        return pagination_serializer_class(instance=page, context=context)


# 归属于认证卖家的商品
def get_auth_seller_entities():
    auth_seller = GKUser.objects.authorized_seller()
    shop_link_list = Shop.objects.filter(owner__in=list(auth_seller)).values_list('common_shop_link', flat=True)
    entities = Entity.objects.filter(buy_links__shop_link__in=list(shop_link_list), status=1, buy_links__status=2)
    return entities


class DesignWeekPaginationSerializer(BasePaginationSerializer):
    total_count = serializers.ReadOnlyField(source='paginator.count')
    page_size = serializers.SerializerMethodField('get_pagesize')
    page_offset = serializers.SerializerMethodField('get_pageoffset')

    def get_pagesize(self, page):
        return int(self.context['request'].query_params.get('page_size'))

    def get_pageoffset(self, page):
        return int(self.context['request'].query_params.get('page_offset'))


class NewPaginationSerializer(DesignWeekPaginationSerializer):
    def __init__(self, *args, **kwargs):
        self.results_field = 'data'
        super(NewPaginationSerializer, self).__init__(*args, **kwargs)
