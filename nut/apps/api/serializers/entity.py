from apps.core.models import Entity
from rest_framework import serializers


class EntitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Entity
        depth = 1



__author__ = 'edison7500'
