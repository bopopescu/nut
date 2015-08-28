import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR+'../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'


from apps.core.models import Tag, Entity_Tag, Event
from apps.tag.models import Tags as NewTag
from apps.tag.models import Content_Tags
from hashlib import md5

# tag
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

# event
events = Event.objects.all()
for row in events:
    print row.tag
    try:
        t = Tag.objects.get(tag_hash=row.tag)
    except Tag.DoesNotExist:
        continue
    row.tag = t.tag
    row.save()

# tag content
et = Entity_Tag.objects.all()
for row in et:
    # print row.entity.notes.get(user=row.user), row.tag
    # try:
    notes = row.entity.notes.filter(user=row.user)
    print notes
    if len(notes) > 0:
        t = NewTag.objects.get(name = row.tag.tag)
        ct = Content_Tags()
        ct.tag = t
        ct.target = notes[0]
        ct.creator = row.user
        ct.created_datetime = row.created_time
        ct.save()
    continue




__author__ = 'edison'
