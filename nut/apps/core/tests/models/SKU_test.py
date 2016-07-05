# coding=utf-8
import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from pprint import  pprint


from apps.core.models import Entity , SKU


# SYNCDB
#### #注意用测试数据库


# 确保ListObject field 可用
e = Entity.objects.get(id='4658141')
e.skus.all().delete()
e.add_sku()
e.add_sku()
e.add_sku(
    {
        'color': 'red',
        'size': '165',
        'gender':'male'
     })
assert(e.skus.all().count() == 2 )

e.add_sku({
        'color': 'black'
    })

assert(e.skus.all().count() == 3 )



e.add_sku({
        'color': 'black'
    })
assert(e.skus.all().count() == 3 )



e.add_sku({
        'limited':'jordan 12'
})

e.add_sku({
        'limited':'jordan 13'
})

assert(e.skus.all().count()==5)

e.add_sku({
    'deficit':'all'
})


assert(e.skus.all().count()==6)