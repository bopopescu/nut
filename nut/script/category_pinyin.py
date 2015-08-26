from xpinyin import Pinyin

import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.stage'


from apps.core.models import Sub_Category


p = Pinyin()

sc = Sub_Category.objects.all()

for row in sc:
    print row.title, p.get_pinyin(row.title.replace('-', ''), '')
    row.alias = p.get_pinyin(row.title.replace('-', ''), '')
    row.save()

__author__ = 'xiejiaxin'
