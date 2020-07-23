import os, sys
sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Selection_Entity, Entity_Like
from apps.report.models import Selection
from datetime import datetime, timedelta


dt = datetime.now()
day = timedelta(days=1)

b = dt - day
date_string = dt.strftime("%Y-%m-%d")
selection = Selection_Entity.objects.raw("select id, count(*) as count from core_selection_entity where is_published = 1 and pub_time BETWEEN '%s' and '%s'" % (b.strftime("%Y-%m-%d"), date_string)).using('subordinate')
# selection = Selection_Entity.objects.raw("select id, count(*) as count from core_selection_entity where is_published = 1 and pub_time BETWEEN '2015-01-27' and '2015-01-28'" )
el = Entity_Like.objects.filter(created_time__range=(b.strftime("%Y-%m-%d"), date_string))
# print selection.query


try:
    s = Selection.objects.get(pub_date=date_string)
    s.selected_total = selection[0].count
    s.like_total = el.count()
    s.save()
except Selection.DoesNotExist:
    s = Selection(
        selected_total = selection[0].count,
        like_total = el.count(),
        pub_date = date_string,
    )
    s.save()

# print b.strftime("%Y-%m-%d")
#
# while True:
#
#     selection = Selection_Entity.objects.raw("select id, count(*) as count from core_selection_entity where is_published = 1 and pub_time BETWEEN '%s' and '%s'" % (b.strftime("%Y-%m-%d"), date_string))
#     if selection[0].count == 0:
#         break
#     s = Selection(
#         selected_total = selection[0].count,
#         pub_date = date_string,
#     )
#     s.save()
#     # print date_string
#     # print selection.query
#     # print selection[0].count
#     dt -= day
#     b -= day
#     date_string = dt.strftime("%Y-%m-%d")
#     print b.strftime("%Y-%m-%d"), date_string
#     # print b
#     if selection[0].count == 0:
#         break

__author__ = 'edison'
