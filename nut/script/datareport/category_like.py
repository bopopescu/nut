# -*- coding: utf-8 -*-
import os, sys
#
# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from datetime import datetime, timedelta
from apps.core.models import Entity_Like, Sub_Category, Category

from django.template import loader, Context





dt  = datetime.now()
time_range = timedelta(days=30)
from_time = (dt-time_range).strftime("%Y-%m-%d") + ' 00:00'


sub_categorys = Sub_Category.objects.all()
sub_category_like_count_list = []

for sub_category in sub_categorys:
    sub_c_count = Entity_Like.objects.using('slave')\
                 .filter(entity__category=sub_category)\
                  .count()

    sub_category_like_count_list.append((sub_category.title , sub_c_count))

result = sorted(sub_category_like_count_list, \
                 key=lambda cat: int(cat[1]), reverse=True)


t = loader.get_template('category/category_like.html')
c = Context({
    'categories': result
})

outfile = open('category_like_list.html', 'w')
outfile.write(t.render(c).encode('utf-8'))
quit()


#category list


# categorys = Category.objects.all()
# category_like_count_list = []
# for category in categorys:
#     c_count = Entity_Like.objects.using('slave')\
#                          .filter(entity__category__group=category)\
#                          .count()
#     category_like_count_list.append((category.title, c_count))
#
# sorted(category_like_count_list, key=lambda cat: cat[1])


outfile = open('category_like_list.html', 'w')
# for c_count_dic in category_like_count_list:
#     outfile.write('%s%s\n'%(c_count_dic[0].encode('utf-8'), c_count_dic[1].encode('utf-8')))

for sc_count_dic in sub_category_like_count_list:
    outfile.write('%s%s\n'%(sc_count_dic[0], sc_count_dic[1]))

outfile.close()