from apps.core.models import GKUser, User_Profile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User_Profile
        fields = ('nickname', 'location', 'city', 'gender', 'bio', 'website', 'avatar', 'email_verified',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    like_count = serializers.IntegerField(source='like_count', read_only=True)
    is_verified = serializers.BooleanField(source='is_verified', read_only=True)
    create_entity_count = serializers.IntegerField(source='create_entity_count', read_only=True)
    # user_profile = serializers.HyperlinkedModelSerializer(source='UserProfileSerializer')
    profile = UserProfileSerializer()

    class Meta:
        model = GKUser
        fields = ('url', 'email', 'like_count', 'profile', 'is_verified', 'create_entity_count')
        # depth = 1

__author__ = 'edison7500'
