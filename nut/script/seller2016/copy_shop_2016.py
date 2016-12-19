# coding=utf-8

import os,sys
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.stage'


#only need run once


from apps.seller.models import Seller_Profile

for sp in Seller_Profile.objects.all():
    sp.is2015store = True
    sp.is2016store = False
    sp.save()
    #dup
    sp.pk = None
    sp.is2015store = False
    sp.is2016store = True
    sp.save()
