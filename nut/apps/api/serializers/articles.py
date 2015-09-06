from rest_framework import serializers


from apps.core.models import Article, Selection_Article,GKUser
from apps.counter.utils.data import RedisCounterMachine
from apps.api.serializers.user import NestingUserSerializer

# the following serializer is for ArticleSerializer nested use only
class NestedSelectionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Article
        fields = ('is_published','create_time','pub_time', )


class ArticleSerializer(serializers.ModelSerializer):
    selections = NestedSelectionArticleSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()
    coverImage = serializers.SerializerMethodField()
    creator = NestingUserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(read_only=False,source='creator',queryset=GKUser.objects.author())

    class Meta:
        model = Article
        fields =  ('id','creator','creator_id','status','title','coverImage','selections','cover','publish','updated_datetime','showcover','read_count','cover_url')

    def get_status(self, obj):
        return obj.get_publish_display()

    def get_coverImage(self,obj):
        return obj.cover_url.replace('images/', 'images/100/')

    def update(self, instance, validated_attrs):
        super(ArticleSerializer, self).update(instance, validated_attrs)
        id = instance.id
        read_count =validated_attrs['read_count']
        RedisCounterMachine.set_article_read_count_from_pk(id, read_count)
        return instance


