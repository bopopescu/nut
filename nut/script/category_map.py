import os, sys
sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from django.core.cache import cache
from apps.core.models import Entity
from hashlib import md5


maping = Entity.objects.raw('select e.id, e.category_id, b.cid, b.origin_source, count(*) from core_entity as e join core_buy_link as b on e.id = b.entity_id where b.cid != -1 group by b.cid').using('subordinate')

for row in maping:
    print row.category_id, row.cid, row.origin_source

    key_string = "%s%s" % (row.cid, row.origin_source)

    key = md5(key_string.encode('utf-8')).hexdigest()
    print key

    cache.set(key, row.category_id, timeout=7200)

__author__ = 'edison'
