from apps.core.models import Friendly_Link
from django import template

register = template.Library()


@register.assignment_tag
def get_friendly_links():
    return Friendly_Link.objects.filter(status=Friendly_Link.enabled)[:16]
