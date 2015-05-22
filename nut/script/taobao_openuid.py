import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Taobao_Token
from apps.core.utils.taobaoapi.user import TaobaoOpenUid

from django.conf import settings

app_key = getattr(settings, 'TAOBAO_APP_KEY')
app_secret = getattr(settings, 'TAOBAO_APP_SECRET')


tusers = Taobao_Token.objects.filter(open_uid__isnull = True)
print tusers.count()
for row in tusers:
    print row.id, row.taobao_id, row.screen_name
    if (row.taobao_id):
        t = TaobaoOpenUid(app_key, app_secret)
        openuid =  t.get_open_id(row.taobao_id)
        print openuid
        row.open_uid = openuid
        row.save()

__author__ = 'edison7500'
