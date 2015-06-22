import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.stage'

from apps.core.models import Buy_Link
import requests
import time


def crawl(item_id):
    data = {
        'project':'default',
        'spider':'taobao',
        'setting':'DOWNLOAD_DELAY=2',
        'item_id': item_id,
    }
    res = requests.post('http://localhost:6800/schedule.json', data=data)
    return res.json()

links = Buy_Link.objects.filter(origin_source='taobao.com')

for row in links[:100]:
    # print row.origin_id
    print row.origin_id, crawl(item_id=row.origin_id)
    time.sleep(5)



__author__ = 'edison'
