# -*- coding: utf-8 -*-

from rest_framework import  serializers
from apps.api.serializers.articles import NestedArticleSerializer
from apps.core.models import Event, Article

class EventSerializer(serializers.ModelSerializer):
    # related_articles = NestedArticleSerializer(many=True, read_only=False)
    class Meta:
        model = Event
        fields = ['id','title','slug', 'related_articles']


