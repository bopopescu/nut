from rest_framework import serializers

from apps.core.models import Friendly_Link

class Friendly_Link_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Friendly_Link
        fields = ('id', 'name', 'link', 'link_category',\
                  'position','status', 'logo', 'logo_url')
