# coding=utf-8
import datetime

import requests
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.conf import settings
from apps.core.models import Selection_Entity, Entity, Buy_Link


class Command(BaseCommand):
    def handle(self, *args, **options):
        num = args[0]
        last_pub_time = Selection_Entity.objects.filter(is_published=True).latest('pub_time').pub_time
        start_pub_time = last_pub_time + datetime.timedelta(days=1)
        start_pub_time = start_pub_time.replace(hour=9, minute=0, second=0, microsecond=0)

        ses = Selection_Entity.objects.filter(is_published=True,
                                              entity__status=Entity.selection,
                                              entity__buy_links__status=Buy_Link.sale,
                                              pub_time__lt=start_pub_time.replace(month=1, day=1),
                                              pub_time__month=start_pub_time.month)
        ses = ses.select_related('entity__likes').annotate(like_count=Count('entity__likes')).order_by('-like_count')

        for se in ses[:num]:
            buy_link = se.entity.buy_links.first()
            data = {
                'project': 'default',
                'spider': 'taobao',
                'setting': 'DOWNLOAD_DELAY=2',
                'item_id': buy_link.origin_id,
            }
            res = requests.post(settings.CHECK_BUY_LINK_URL, data=data)
            self.stdout.write(u'{}: {}'.format(se.entity.title, res.text))
