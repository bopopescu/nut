import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.stage'


from apps.core.models import Tag
from apps.tag.models import Tags as NewTag
from hashlib import md5


tags = Tag.objects.all()
print tags.count()
for row in tags:
    print row.tag, md5(row.tag.encode('utf-8')).hexdigest(), row.creator_id, row.status
    # print md5(row.tag.encode('utf-8')).hexdigest()
    nt = NewTag()
    nt.name = row.tag
    nt.hash = md5(row.tag.encode('utf-8')).hexdigest()
    nt.status = row.status
    nt.save()

__author__ = 'edison'
