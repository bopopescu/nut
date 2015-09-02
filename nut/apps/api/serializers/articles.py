from rest_framework import serializers

from apps.core.models import Article, Selection_Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields =  ('id','creator','title','cover', 'content','published','created_datetime','showcover','read_count','cover_url')


class SelectionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Article
        fields = ('article', 'is_published', 'pub_time')

