import os, sys
sys.path.append('/data/www/nut')
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
    # print buy_link['cid']
    # print buy_link['entity_id']
    # print buy_link['taobao_id']
    # print buy_link['source']
    if buy_link:

        taobao_id = buy_link.get('taobao_id', None)
        if taobao_id:
            link = 'http://item.%s.com/item.htm?id=%s' % (buy_link.get('source', None), buy_link.get('taobao_id', None))
            host = "%s.com" % buy_link['source']
            # print link, host
            Buy_Link.objects.create(
                entity_id = row.pk,
                origin_id = buy_link['taobao_id'],
                cid = buy_link['cid'],
                origin_source = host,
                link = link,
                price = buy_link.get('price', 0),
            )
        elif buy_link.get('jd_id'):
            link = 'http://item.%s.com/%s.html' %  (buy_link.get('source', None), buy_link.get('jd_id', None))
            host = "%s.com" % buy_link['source']
            # print buy_link['jd_id'], host
            Buy_Link.objects.create(
                entity_id = row.pk,
                origin_id = buy_link['jd_id'],
                cid = buy_link['cid'],
                origin_source = host,
                link = link,
                price = buy_link.get('price', 0),
            )
        else:
            continue





__author__ = 'edison'
