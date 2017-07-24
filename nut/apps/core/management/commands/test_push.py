# coding=utf-8
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.core.models import GKUser
import jpush

app_key = getattr(settings, 'JPUSH_KEY', None)
app_secret = getattr(settings, 'JPUSH_SECRET', None)


class Command(BaseCommand):
    help = 'test jpush'

    def handle(self, *args, **options):
        user = GKUser.objects.get(pk=2067879)
        rids = list(user.jpush_token.all().values_list('rid', flat=True))
        _jpush = jpush.JPush(app_key, app_secret)
        push = _jpush.create_push()
        extras = {
            'url': 'http://www.guoku.com/detail/03071d5f/'
        }
        push.notification = jpush.notification(alert='推送测试',
                                               ios=jpush.ios('iOS推送测试', extras=extras),
                                               android=jpush.android('Android推送测试', extras=extras))
        push.platform = jpush.all_
        push.audience = jpush.registration_id(*rids)
        push.options = {'apns_production': False}
        print(push.payload)

        push.send()
