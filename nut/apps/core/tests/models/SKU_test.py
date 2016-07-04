# coding=utf-8
import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from pprint import  pprint


from apps.core.models import Entity , SKU

e = Entity.objects.get(id='4658141')
e.sku_attributes = [
    {'color': ['red', 'blue', 'black', 'red']},
    {'size': ['168', '175', '180']},
    {'gender': ['male', 'female']}
]
e.save()

f = Entity.objects.get(id='4658141')
pprint(f.sku_attributes)


# 空白SKU attributes , is None

g = Entity.objects.get(id='4658142')
assert(g.sku_attributes is None)

g.generate_sku_list()

e.generate_sku_list()



