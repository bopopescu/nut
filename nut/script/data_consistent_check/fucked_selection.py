# coding=utf-8

import os,sys
import csv

sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from apps.core.models import Selection_Entity, Entity, Note


last_entity = Entity.objects.get(entity_hash='f0489369')
end_entity = Entity.objects.get(entity_hash='0c06027f')

id = last_entity.pk
end_id=end_entity.pk

entities = Entity.objects.filter(pk__gt=id, pk__lt=end_id)

s_entities = Selection_Entity.objects.filter(entity__in=entities).values_list('entity__id')

len(s_entities)

final_s_entity =  Entity.objects.filter(pk__in=s_entities)

fields = ['absolute_url' , 'title', 'top_note_string']
writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)

for entity in final_s_entity:
    note = ''
    try :
        note = entity.top_note.note
    except Exception as e :
        pass

    url = 'www.guoku.com' + entity.absolute_url
    title = entity.title


    writer.writerow([
        url.encode('utf-8'),
        title.encode('utf-8'),
        note.encode('utf-8')
    ])




