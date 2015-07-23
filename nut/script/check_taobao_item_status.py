import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Buy_Link, Entity
import requests
import time


def crawl(item_id):
    data = {
        'project':'default',
        'spider':'taobao',
        'setting':'DOWNLOAD_DELAY=2',
        'item_id': item_id,
    }
    res = requests.post('http://10.0.2.48:6800/schedule.json', data=data)
    return res.json()

links = Buy_Link.objects.filter(origin_source='taobao.com', entity__status__gt=Entity.new).exclude(status=Buy_Link.remove).order_by('-id')
# print links.count()
for row in links:
    print row.origin_id, crawl(item_id=row.origin_id)
    time.sleep(5)



__author__ = 'edison'
