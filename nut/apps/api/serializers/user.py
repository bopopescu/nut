from apps.core.models import GKUser
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    like_count = serializers.IntegerField(source='like_count', read_only=True)
    is_verified = serializers.BooleanField(source='is_verified', read_only=True)
    create_entity_count = serializers.IntegerField(source='create_entity_count', read_only=True)

    class Meta:
        model = GKUser
        fields = ('id', 'url', 'email', 'like_count', 'profile', 'is_verified', 'create_entity_count')
        depth = 1

__author__ = 'edison7500'
