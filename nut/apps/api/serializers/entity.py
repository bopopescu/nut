# coding=utf-8
from urlparse import urljoin

from apps.core.models import Entity, GKUser, Entity_Like
from django.core.paginator import Paginator
from rest_framework import serializers, pagination
from apps.api.serializers.user import WebUserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GKUser
        fields = ('email', 'nickname',)


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Entity
        fields = ('user', 'url', 'brand', 'title', 'intro', 'rate',
                  'price', 'status', 'chief_image', 'detail_images', 'like_count', 'note_count')


# for web front use
class WebEntityLikeSerializer(serializers.ModelSerializer):
    user = WebUserSerializer()

    class Meta:
        model = Entity_Like
        fields = ('user',)


class PaginatedEntityLikeSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = WebEntityLikeSerializer


# the following serializer is for web's entity detail page
class WebEntitySerializer(serializers.ModelSerializer):
    # only return the first 30 entity likes for performance reason,
    limited_likers = serializers.SerializerMethodField(method_name='limited_likers_method')

    class Meta:
        model = Entity
        fields = ('id', 'title', 'limited_likers')

    def limited_likers_method(self, obj):
        # already sorted by created date,
        current_page = Paginator(obj.likes.all(), 21).page(1)
        serializer = PaginatedEntityLikeSerializer(current_page)

        return serializer.data


class SkuSerializer(serializers.ModelSerializer):
    sku_id = serializers.CharField(source='entity_hash')
    tp_src = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    desc = serializers.CharField(source='intro')
    img = serializers.CharField(source='chief_image')
    price = serializers.SerializerMethodField()
    mprice = serializers.SerializerMethodField()
    promotion_url = serializers.SerializerMethodField()

    def get_tp_src(self, obj):
        return 'guocool'

    def get_source(self, obj):
        return u'淘宝'

    def get_price(self, obj):
        return int(obj.price * 100)

    def get_mprice(self, obj):
        return int(obj.price * 100)

    def get_is_on_sale(self, obj):
        return True

    def get_promotion_url(self, obj):

        return urljoin('http://www.guoku.com', obj.absolute_url)

    class Meta:
        model = Entity
        fields = ('sku_id', 'tp_src', 'source', 'is_on_sale', 'name', 'desc', 'img', 'price', 'mprice',
                  'promotion_url',)
