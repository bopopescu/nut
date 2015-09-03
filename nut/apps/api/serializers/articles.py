from rest_framework import serializers

from apps.core.models import Article, Selection_Article


class ArticleSerializer(serializers.ModelSerializer):
    selections = NestedSelectionArticleSerializer
    class Meta:
        model = Article
        fields =  ('id','creator','selections','title','cover', 'content','published','created_datetime','showcover','read_count','cover_url')

# the following serializer is for ArticleSerializer nested use only
class NestedSelectionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Article
        fields = ('is_published','create_time','pub_time', )

