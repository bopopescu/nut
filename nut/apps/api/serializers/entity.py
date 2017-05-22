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
