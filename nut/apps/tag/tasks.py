#coding=utf-8
from celery.task import task
from apps.core.tasks import BaseTask
from django.core import serializers

from apps.tag.lib.tag import TagParser
from apps.tag.models import Tags, Content_Tags
from apps.core.models import Note, Article


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
                print tag.name
                try:
                    c = Content_Tags.objects.get(tag=tag, creator=obj.user, target_content_type=24, target_object_id=obj.id)
                except Content_Tags.DoesNotExist:
                    c = Content_Tags()
                    c.target = obj
                    c.tag = tag
                    c.creator = obj.user
                    c.save()

    if isinstance(obj, Article):
        print obj.content

    return

__author__ = 'xiejiaxin'
