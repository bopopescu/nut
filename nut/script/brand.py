import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.stage'

from apps.core.models import Entity, Brand

brands = Entity.objects.raw("select id, brand, count(*) from core_entity where brand !='' and status != -1  group by brand")

for row in brands:
    print row.brand.strip()

    b = Brand()
    b.name = row.brand.strip()
    try:
        b.save()
    except Exception, e:
        print e.message
        pass

__author__ = 'edison'
