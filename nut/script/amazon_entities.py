# coding=utf-8

import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from apps.core.models import Buy_Link, Entity
import csv

def run():
    amazon_entity_ids = Buy_Link.objects\
                                .filter(origin_source__icontains='amazon')\
                                .values_list('entity_id', flat=True)
    entities  =  Entity.objects.filter(pk__in=amazon_entity_ids)
    fields = ['brand','title','top_note','buy_link','guoku_link','price','created_time']

    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    writer.writerow(fields)
    for entity  in entities:
        note = ''
        try :
            note = entity.top_note.note
        except Exception as e :
            pass

        writer.writerow([entity.brand.encode('utf-8'),
                         entity.title.encode('utf-8'),
                         note.encode('utf-8'),
                         entity.default_buy_link.link.encode('utf-8'),
                         'http://www.guoku.com'+entity.absolute_url.encode('utf-8'),
                         entity.default_buy_link.price,entity.created_time])


run()