# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.core.models import Article, Selection_Article,GKUser
from apps.counter.utils.data import RedisCounterMachine
from apps.api.serializers.user import NestingUserSerializer

import re
import json
from apps.tag.tasks import generator_article_tag

# the following serializer is for ArticleSerializer nested use only
class NestedSelectionArticleSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Article.objects.all())
    class Meta:
        model = Selection_Article
        fields = ('article','is_published','create_time','pub_time', )


class NestedArticleSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    creator = NestingUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id','creator','title')

    def get_coverImage(self,obj):
        return obj.cover_url.replace('images/', 'images/100/')


class ArticleSerializer(serializers.ModelSerializer):
    selections = NestedSelectionArticleSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()
    coverImage = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField(read_only=False)
    creator = NestingUserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(read_only=False,source='creator',queryset=GKUser.objects.author())

    class Meta:
        model = Article
        fields =  ('id','creator'\
                       ,'tags','creator_id','status','title'\
                       ,'coverImage','selections'\
                       ,'once_selection','cover'\
                       ,'publish','updated_datetime'\
                       ,'last_selection_time','showcover'\
                       ,'read_count','cover_url')

    def get_status(self, obj):
        return obj.get_publish_display()

    def get_coverImage(self,obj):
        return obj.cover_url.replace('images/', 'images/100/')

    def get_tags(self, obj):
        tags = obj.tag_list
        return ','.join([tag for tag in tags])

    def update(self, instance, validated_attrs):
        super(ArticleSerializer, self).update(instance, validated_attrs)
        _tags = self._initial_data['tags']
        _tags = _tags.strip()
        _tags = _tags.replace(u'，',',')
        _tags = _tags.replace(u'＃','#')
        _tmp_tags = re.split(',|\s|#', _tags)
        res = list()
        for row in _tmp_tags:
            if len(row) == 0:
                continue
            res.append(row)
        res = list(set(res))
        if res:
            data = {
                'tags':res,
                'article': instance.id
            }
            generator_article_tag(data=json.dumps(data))
        id = instance.id
        read_count =validated_attrs['read_count']
        RedisCounterMachine.set_article_read_count_from_pk(id, read_count)
        return instance


