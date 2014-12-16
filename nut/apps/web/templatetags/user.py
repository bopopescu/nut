from django.utils.log import getLogger
from django import template

from apps.core.models import User_Profile

register = template.Library()
log = getLogger('django')


def nickname(value):
    profile = User_Profile.objects.get(user_id = value)

    return profile.nickname

register.filter(nickname)


__author__ = 'edison'
