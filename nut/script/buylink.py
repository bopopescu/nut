import os, sys
sys.path.append('/Users/edison/PycharmProjects/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from pymongo import MongoClient

from django.conf import settings
client = MongoClient('mongodb://10.0.2.200:27017/')
db = client.guoku
collection = db.item


from apps.core.models import Entity
from apps.core.models import Buy_Link

entities = Entity.objects.all()

for row in entities:
    # print row.pk
    buy_link =  collection.find_one({'entity_id':row.pk})
    # print buy_link['price']
    # print buy_link['entity_id']
    # print buy_link['taobao_id']
    # print buy_link['source']
    link = 'http://item.%s.com/item.htm?id=%s' %  (buy_link['source'], buy_link['taobao_id'])
    host = "%s.com" % buy_link['source']
    print link, host

    if buy_link:
        Buy_Link.objects.create(
            entity_id = row.pk,
            origin_id = buy_link['taobao_id'],
            origin_source = buy_link['source'],
            link = link,
            price = buy_link.get('price', 0),
        )


__author__ = 'edison'
