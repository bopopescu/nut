import os, sys
sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Entity_Like
from apps.report.models import Selection
from datetime import datetime, timedelta

dt = datetime.now()
day = timedelta(days=1)

b = dt - day
date_string = dt.strftime("%Y-%m-%d")
# el = Entity_Like.objects.filter(created_time__range=(b.strftime("%Y-%m-%d"), date_string))
#
# print el.count()



while True:

    # selection = Selection_Entity.objects.raw("select id, count(*) as count from core_selection_entity where is_published = 1 and pub_time BETWEEN '%s' and '%s'" % (b.strftime("%Y-%m-%d"), date_string))
    el = Entity_Like.objects.filter(created_time__range=(b.strftime("%Y-%m-%d"), date_string))
    if el.count() == 0:
        break


    try:
        s= Selection.objects.get(pub_date=date_string)
        s.like_total = el.count()
        # s.save()
    except Selection.DoesNotExist:
        s = Selection(
            like_total = el.count(),
            pub_date = date_string,
        )
    finally:
        s.save()

    dt -= day
    b -= day
    date_string = dt.strftime("%Y-%m-%d")
    print b.strftime("%Y-%m-%d"), date_string, el.count()
    # print b
    # if el[0].count == 0:
    #     break



__author__ = 'edison'
