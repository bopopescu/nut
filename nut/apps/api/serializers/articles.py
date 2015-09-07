from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from apps.tag.models import Content_Tags


from apps.core.models import Article, Selection_Article,GKUser
from apps.counter.utils.data import RedisCounterMachine
from apps.api.serializers.user import NestingUserSerializer

import re
import json
from apps.tag.tasks import generator_article_tag

# the following serializer is for ArticleSerializer nested use only
class NestedSelectionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Article
        fields = ('is_published','create_time','pub_time', )


class ArticleSerializer(serializers.ModelSerializer):
    selections = NestedSelectionArticleSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()
    coverImage = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField(read_only=False)
    creator = NestingUserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(read_only=False,source='creator',queryset=GKUser.objects.author())

    class Meta:
        model = Article
        fields =  ('id','creator','tags','creator_id','status','title','coverImage','selections','cover','publish','updated_datetime','showcover','read_count','cover_url')

    def get_status(self, obj):
        return obj.get_publish_display()

    def get_coverImage(self,obj):
        return obj.cover_url.replace('images/', 'images/100/')

    def get_tags(self, obj):
        tags = Content_Tags.objects\
                            .filter(target_object_id=obj.id, target_content_type=ContentType.objects.get_for_model(obj))\
                            .values('tag__name')\
                            .distinct()
        return ','.join([tag['tag__name'] for tag in tags])

    def validate_tags(self, value):
        _tags = value
        _tags = _tags.strip()
        _tmp_tags = re.split(',|\s', _tags)
        # _tags = _tags.split(', ')
        res = list()
        for row in _tmp_tags:
            if len(row) == 0:
                continue
            res.append(row)
        return res


    def update(self, instance, validated_attrs):
        super(ArticleSerializer, self).update(instance, validated_attrs)
        tags = validated_attrs['tags']
        if tags:
            data = {
                'tags':tags,
                'article': instance.id
            }
            generator_article_tag(data=json.dumps(data))
        id = instance.id
        read_count =validated_attrs['read_count']
        RedisCounterMachine.set_article_read_count_from_pk(id, read_count)
        return instance


