from rest_framework import serializers

from apps.core.models import Sidebar_Banner

class Sidebar_Banner_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sidebar_Banner
        fields = ('id','image','image_url','position','updated_time','link', 'status')