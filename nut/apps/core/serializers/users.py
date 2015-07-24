from rest_framework import serializers
from apps.core.models import  GKUser, Article ,User_Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('user','nickname','gender','bio','website', 'avatar')

class GKUserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = GKUser
        fields =('id', 'is_active', 'is_admin', 'profile', 'articles')

