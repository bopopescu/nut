from django.utils.log import getLogger
from django import template

from apps.core.models import Entity_Tag

register = template.Library()
log = getLogger('django')


def display_tags_entity(tag_id, user_id):

    _entities = Entity_Tag.objects.filter(tag_id=tag_id, user_id=user_id)

    return {
        "entities":_entities[:4]
    }
register.inclusion_tag("web/account/partial/tag_entities.html")(display_tags_entity)

__author__ = 'edison'
