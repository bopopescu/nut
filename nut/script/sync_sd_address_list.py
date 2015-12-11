#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gc


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR + '../')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from apps.core.models import GKUser


def queryset_iterator(queryset, chunksize=100):
    '''''
    Iterate over a Django Queryset ordered by the primary key
    This method loads a maximum of chunksize (default: 100) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    Note that the implementation of the iterator does not support ordered query sets.
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

reload(sys)
sys.setdefaultencoding('utf-8')
file_count = 1
user_count = 0
user_step = 100000

out_file = open('/Users/judy/Desktop/address_lists/test_%d.txt' % file_count, 'w')
# all_gkusers = GKUser.objects
all_gkusers = GKUser.objects.filter(is_active__gt=GKUser.remove, profile__email_verified=True)
for user in queryset_iterator(all_gkusers):
    if user_count == user_step or (user_count > user_step and user_count % user_step == 0):
        out_file.close()
        file_count += 1
        out_file = open('/Users/judy/Desktop/address_lists/test_%d.txt' % file_count, 'w')
    nickname = user.nickname or user.email
    out_file.write('%s<%s>' % (nickname.encode(), user.email))
    out_file.write('\n')
    user_count += 1
    print user_count, nickname

print '> user_count: ', user_count
out_file.close()
