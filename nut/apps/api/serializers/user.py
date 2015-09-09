from apps.core.models import GKUser, User_Profile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('nickname', 'location', 'city', 'gender', 'bio', 'website', 'avatar', 'email_verified',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    create_entity_count = serializers.IntegerField(read_only=True)
    # user_profile = serializers.HyperlinkedModelSerializer(source='UserProfileSerializer')
    profile = UserProfileSerializer()

    class Meta:
        model = GKUser
        fields = ('id','url', 'email', 'like_count', 'profile', 'is_verified', 'create_entity_count')
        # depth = 1


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.FileField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(AvatarSerializer, self).__init__(*args, **kwargs)


    def save(self, **kwargs):
        _avarar = self.validated_data.get('avatar')


class NestingUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = GKUser
        fields = ('id','profile','email')


__author__ = 'edison7500'
