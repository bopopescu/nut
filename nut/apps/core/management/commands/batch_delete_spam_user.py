# coding=utf-8
from __future__ import print_function

from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.core.models import GKUser


class Command(BaseCommand):
    help = 'clean all blocked user\'s data'

    def handle(self, *args, **options):
        users = GKUser.objects.filter(date_joined__gte='2017-01-01', is_active__gt=0)
        for keyword in args:
            keyword = keyword.decode('utf-8')
            keyword_filter = Q(profile__nickname__icontains=keyword) | Q(profile__bio__icontains=keyword)
            need_delete_users = users.filter(keyword_filter)
            print(u'-' * 40)
            print(u'关键词： {}'.format(keyword))
            for user in need_delete_users:
                print(u'{}:  {}'.format(str(user.date_joined), user.profile.nickname))
            if need_delete_users.count() > 0:
                print(u'关键词： {}, 共{}个，是否确认全部删除？ (yes/no): '.format(keyword, need_delete_users.count()), end='')
                choice = raw_input().lower()
                if choice == 'yes':
                    delete_amount = users.filter(keyword_filter).update(is_active=-1)
                    print(u'已全部删除，共删除{}个'.format(delete_amount))
                else:
                    print(u'命令取消')
            else:
                print(u'无结果')
