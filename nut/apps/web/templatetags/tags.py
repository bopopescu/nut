from django.utils.log import getLogger
from django import template

# from apps.core.models import Entity_Tag
from apps.tag.models import Content_Tags

register = template.Library()
log = getLogger('django')


def display_tags_entity(tag_id, user_id=None):
    if user_id:
        _content_tags = Content_Tags.objects.filter(tag_id=tag_id, creator_id=user_id, target_content_type_id=24)
    else:
        _content_tags = Content_Tags.objects.filter(tag_id=tag_id, target_content_type_id=24)

    entities = list()
    for row in _content_tags[:4]:
        entities.append(
            row.target.entity
        )

    return {
        'entities': entities,
    }
    # return {
    #     "entities":_entities[:4]
    # }
register.inclusion_tag("web/account/partial/tag_entities.html")(display_tags_entity)

__author__ = 'edison'
