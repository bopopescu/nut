# coding=utf-8
import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from pprint import  pprint


from apps.core.models import Entity , SKU


#---------
# UPDATE DATABASE :
#
# ALTER TABLE `core`.`core_entity`
# ADD COLUMN `sku_attributes` LONGTEXT NULL DEFAULT NULL AFTER `updated_time`;

# SYNCDB



#
#
# 1.  Entity model 加入一个 ListObject 字段
#
#         sku_attributes = ListObjectField()
#
#     这个字段记录该商品所有的 属性名称,和属性值选项
#
#     例如
#
#     e.sku_attributes = [
#             {'color': ['red', 'blue', 'black', 'red']},
#             {'size': ['168', '175', '180']},
#             {'gender': ['male', 'female']}
#         ]
#
# 2.  新建 SKU model ,
#
#     class SKU(BaseModel):
#         SKU_STATUS_CHOICE = [(disable, _('disable')), (enable, _('enable'))]
#         entity = models.ForeignKey(Entity, related_name='skus')
#         attribute = models.TextField()
#         stock = models.IntegerField(default=0,db_index=True)#库存
#         origin_price = models.FloatField(default=0, db_index=True)
#         promo_price = models.FloatField(default=0, db_index=True)
#         status =  models.IntegerField(choices=SKU_STATUS_CHOICE, default=enable)
#         is_simple = models.BooleanField(default=True)  #是否是简单sku(没有属性组合)
#
#
#     其中, attribute 储存 该 SKU 的属性组合
#     如果 Entity 属性组合如上, 则共会生成 4 * 3 * 2 = 24 个 SKU
#     is_simple = False (非简单SKU)
#
#     其中一个 的SKU 的 attribute 值如下 blue_168_male ,
#     这样的 SKU共有 24 个
#
#     如果 Entity 没有属性(sku_attributes 为空)
#     则只生成一个 SKU , attribute 字段也唯恐, is_simple = True
#     (简单 SKU)



#### #注意用测试数据库


# 确保ListObject field 可用
e = Entity.objects.get(id='4658141')
e.sku_attributes = [
    {'color': ['red', 'blue', 'black', 'red']},
    {'size': ['168', '175', '180']},
    {'gender': ['male', 'female']}
]
e.save()

f = Entity.objects.get(id='4658141')
pprint(f.sku_attributes)


# 空白sku_attributes , 会生成 简单SKU
g = Entity.objects.get(id='4658142')
assert(g.sku_attributes is None)
g.generate_sku_list()


# 非空白 会生成 24 个 SKU
e.generate_sku_list()



