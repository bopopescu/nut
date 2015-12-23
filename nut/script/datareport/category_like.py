# -*- coding: utf-8 -*-
import os, sys
#
# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from apps.core.models import Entity_Like, Sub_Category, Category


sub_categorys = Sub_Category.objects.all()
sub_category_like_count_list = []

for sub_category in sub_categorys:
    sub_c_count = Entity_Like.objects.using('slave')\
                 .filter(entity__category=sub_category).count()
    sub_category_like_count_list.append((sub_category.title , sub_c_count))

sorted(sub_category_like_count_list, key=lambda cat: cat[2])


#category list
categorys = Category.objects.all()
category_like_count_list = []
for category in categorys:
    c_count = Entity_Like.objects.using('slave')\
                         .filter(entity__category__group=category)\
                         .count()
    category_like_count_list.append((category.title, c_count))

sorted(category_like_count_list, key=lambda cat: cat[2])


outfile = open('category_like_list.txt', 'w')
for c_count_dic in category_like_count_list:
    outfile.write(c_count_dic)

for sc_count_dic in sub_category_like_count_list:
    outfile.write(sc_count_dic)

outfile.close()