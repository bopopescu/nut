import os, sys
sys.path.append('/data/www/nut/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from django.db import models
from apps.core.models import Entity_Like, Category, Entity

# Entity.objects.filter()
entity_list = Entity_Like.objects.sort_with_list(category_id=10)


__author__ = 'edison'
