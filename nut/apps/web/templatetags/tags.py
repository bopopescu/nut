# coding=utf-8
from django import template

from apps.tag.models import Content_Tags

register = template.Library()


def display_tags_entity(tag_id, user_id=None):
    if user_id:
        _content_tags = Content_Tags.objects.filter(tag_id=tag_id, creator_id=user_id, target_content_type_id=24)
    else:
        _content_tags = Content_Tags.objects.filter(tag_id=tag_id, target_content_type_id=24)

    return {'entities': [row.target.entity for row in _content_tags[:4]]}


register.inclusion_tag("web/account/partial/tag_entities.html")(display_tags_entity)
