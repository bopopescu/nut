import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Taobao_Token
from apps.core.utils.taobaoapi.user import TaobaoOpenUid, TaobaoOpenIsvUID

from django.conf import settings

app_key = getattr(settings, 'TAOBAO_APP_KEY')
app_secret = getattr(settings, 'TAOBAO_APP_SECRET')


tusers = Taobao_Token.objects.filter(open_uid__isnull=False, isv_uid__isnull=True)
print tusers.count()
# for row in tusers:
#     print row.id, row.taobao_id, row.screen_name
#     if (row.taobao_id):
#         t = TaobaoOpenUid(app_key, app_secret)
#         openuid = t.get_open_id(row.taobao_id)
#         print openuid
#         row.open_uid = openuid
#         row.save()

for row in tusers:
    t = TaobaoOpenIsvUID(app_key, app_secret)
    isv_uid = t.get_isv_uid(row.open_uid)
    print row.open_uid, isv_uid
    row.isv_uid = isv_uid
    row.save()

__author__ = 'edison7500'


