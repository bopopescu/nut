from apps.core.models import Banner
from rest_framework import serializers


class BannerSerializer(serializers.HyperlinkedModelSerializer):

    # url = serializers.URLField(source='url', read_only=True)
    # image_url = serializers.URLField(source='image_url', read_only=True)

    class Meta:
        model = Banner
        fields = ('url', 'image_url')


__author__ = 'edison'
