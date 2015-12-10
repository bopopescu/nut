from apps.core.models import Entity, GKUser, Entity_Like
from django.core.paginator import Paginator
from rest_framework import serializers, pagination
from apps.api.serializers.user import WebUserSerializer

class UserSerializer(serializers.ModelSerializer):

    #nickname = serializers.CharField(source='nickname')

    class Meta:
        model = GKUser
        fields = ('email','nickname',)


class EntitySerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()
    url = serializers.URLField(source='get_absolute_url')
    # chief_image = serializers.URLField(source='chief_image')
    # detail_images = serializers.CharField(source='detail_images')
    # like_count = serializers.IntegerField(source='like_count', read_only=True)
    # note_count = serializers.IntegerField(source='note_count', required=True)
    # entity_hash = serializers.CharField(source='entity_hash', read_only=True)
    # creator = serializers.CharField(source='user')

    class Meta:
        model = Entity
        fields = ('user', 'url', 'brand', 'title', 'intro', 'rate',
                  'price', 'status', 'chief_image', 'detail_images', 'like_count', 'note_count' )
        # depth = 1




# for web front use
class WebEntityLikeSerializer(serializers.ModelSerializer):
    user = WebUserSerializer()
    class Meta:
        model = Entity_Like
        fields = ('user',)

class PaginatedEntityLikeSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = WebEntityLikeSerializer

#  the following serializer is for web's entity detail page
class WebEntitySerializer(serializers.ModelSerializer):
    #only return the first 30 entity likes for performance reason,
    limited_likers = serializers.SerializerMethodField(method_name='limited_likers_method')
    # likes =  WebEntityLikeSerializer(many=True)
    class Meta:
        model = Entity
        fields = ('id', 'title', 'limited_likers')

    def limited_likers_method(self, obj):
        # already sorted by created date,
        thePage = Paginator(obj.likes.all(), 30).page(1)
        serializer = PaginatedEntityLikeSerializer(thePage)

        return serializer.data

__author__ = 'edison7500'
