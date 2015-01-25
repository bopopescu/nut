import os, sys
sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from pymongo import MongoClient

from django.conf import settings
from django.utils.log import getLogger
from apps.core.models import Selection_Entity

log = getLogger('django')

client = MongoClient('mongodb://10.0.2.200:27017/')
db = client.guoku
collection = db.selection

for row in collection.find():
    print row['entity_id'], row['post_time'].strftime("%Y-%m-%d %H:%M:%S")
    s = Selection_Entity(
        entity_id = row['entity_id'],
        pub_time = row['post_time'].strftime("%Y-%m-%d %H:%M:%S"),
    )
    # s.is_published = True
    try:
        s.save()
    except Exception, e:
        log.info(e.message)
        continue
__author__ = 'edison'
