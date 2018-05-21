# coding=utf-8
import arrow
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.core.models import Entity_Like


def update_popular_cache(days):
    time_query_str = arrow.now().shift(days=-days).format('YYYY-MM-DD')
    active_users = get_user_model()._default_manager.filter(is_active__gt=0).values_list('id', flat=True)
    popular_ids = Entity_Like.objects.filter(created_time__gte=time_query_str, user_id__in=active_users) \
                      .values_list('entity', flat=True) \
                      .annotate(dcount=Count('entity')) \
                      .order_by('-dcount')[:400]

    key = 'entity:popular:{}'.format(days)
    cache.set(key, popular_ids, 86400)

    return True


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_popular_cache(7)
