# coding=utf-8
from __future__ import print_function

import re
from django.core.management.base import BaseCommand

import arrow
from apps.core.models import Entity
from utils.open_search_api import V3Api
from utils.utils import chunks
from django.conf import settings

api = V3Api(endpoint=settings.OPEN_SEARCH_ENDPOINT, access_key=settings.OPEN_SEARCH_ACCESS_KEY_ID,
            secret=settings.OPEN_SEARCH_ACCESS_KEY_SECRET, app_name=settings.OPEN_SEARCH_APP_NAME)


class Command(BaseCommand):

    def handle(self, *args, **options):
        num = int(args[0]) if args else 10
        entities = Entity.objects.filter(
            status__gte=0,
            is_sync=False,
        ).order_by('-created_time')
        pass
