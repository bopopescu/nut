#coding=utf-8
from celery.task import task
from apps.core.tasks import BaseTask
from django.core import serializers

from apps.tag.lib.tag import TagParser
from apps.tag.models import Tags, Content_Tags
from apps.core.models import Note, Article
from hashlib import md5
import json


@task(base=BaseTask)
def generator_tag(**kwargs):
    data = kwargs.pop('data', None)
    assert data is not None

    row = next(serializers.deserialize('json', data))
    obj = row.object

    if isinstance(obj, Note):
        t = TagParser(obj.note)

        t_objs = Content_Tags.objects.filter(creator=obj.user, target_content_type=24, target_object_id=obj.id)
        for row in t_objs:
            if row.tag.hash in t.thashs:
                continue
            row.delete()

        for k, v in t.tags.items():
            try:
                tag = Tags.objects.get(hash = v[1])
            except Tags.DoesNotExist:
                tag = Tags()
                tag.name = v[0]
                tag.hash = v[1]
                tag.save()
            finally:
                # print tag.name
                try:
                    c = Content_Tags.objects.get(tag=tag, creator=obj.user, target_content_type=24, target_object_id=obj.id)
                except Content_Tags.DoesNotExist:
                    c = Content_Tags()
                    c.target = obj
                    c.tag = tag
                    c.creator = obj.user
                    c.save()

    # if isinstance(obj, Article):
    #     print obj.content
    #
    # return


@task(base=BaseTask)
def generator_article_tag(**kwargs):
    data = kwargs.pop('data', None)
    assert data is not None
    data = json.loads(data)
    aid = data['article']
    # print data['tags']
    try:
        article = Article.objects.get(pk = aid)
    except Article.DoesNotExist:
        raise

    tag_hash_list = list()
    for row in data['tags']:
        row = row.lower().strip()
        tag_hash_list.append(md5(row.encode('utf-8')).hexdigest())

    # print tag_hash_list
    t_objs = Content_Tags.objects.filter(creator=article.creator, target_content_type=31, target_object_id=article.id)
    for row in t_objs:
        if row.tag.hash in tag_hash_list:
            print row.tag.hash
            continue
        row.delete()

    for row in data['tags']:
        tag = row.lower().strip()
        thash = md5(tag.encode('utf-8')).hexdigest()
        # print thash, tag
        try:
            t = Tags.objects.get(hash = thash)
        except Tags.DoesNotExist:
            t = Tags()
            t.name = tag
            t.hash = thash
            t.save()
        finally:
            try:
                c = Content_Tags.objects.get(tag=t, creator=article.creator, target_content_type=31, target_object_id=article.id)
            except Content_Tags.DoesNotExist:
                c = Content_Tags()
                c.target = article
                c.tag = t
                c.creator = article.creator
                c.save()


__author__ = 'xiejiaxin'
