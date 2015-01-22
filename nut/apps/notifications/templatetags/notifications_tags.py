# -*- coding: utf-8 -*-
from django.template import Library
from django.template.base import TemplateSyntaxError
from django.template import Node

register = Library()


from django.utils.log import getLogger
log = getLogger('django')

@register.assignment_tag(takes_context=True)
def notifications_unread(context):
    if 'user' not in context:
        return ''

    user = context['user']
    log.info(user.notifications.read())
    if user.is_anonymous():
        return ''
    return user.notifications.unread().count()