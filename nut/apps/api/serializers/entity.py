from apps.core.models import Entity, GKUser
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):

    #nickname = serializers.CharField(source='nickname')

    class Meta:
        model = GKUser
        fields = ('email','nickname')


class EntitySerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()
    # chief_image = serializers.URLField(source='chief_image')
    # detail_images = serializers.CharField(source='detail_images')
    # like_count = serializers.IntegerField(source='like_count', read_only=True)
    # note_count = serializers.IntegerField(source='note_count', required=True)
    # entity_hash = serializers.CharField(source='entity_hash', read_only=True)
    # creator = serializers.CharField(source='user')

    class Meta:
        model = Entity
        fields = ('user', 'url', 'entity_hash', 'brand', 'title', 'intro', 'rate',
                  'price', 'status', 'chief_image', 'detail_images', 'like_count', 'note_count' )
        # depth = 1



__author__ = 'edison7500'
