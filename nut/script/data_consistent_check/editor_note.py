# coding=utf-8

import os,sys
import csv

sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from apps.core.models import Selection_Entity, Entity, Note, GKUser


editors =  GKUser.objects.editor()
fucked_note = Note.objects.filter(pk__gt=799866, user__in=editors)

#
# fucked_note_entities_ids = fucked_note.values_list('entity__id', flat=True)
# entities = Entity.objects.filter(pk__in=fucked_note_entities_ids)


len(fucked_note)

fields = ['note' ,'user','user_id', 'title', 'entity_url']
writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)

for note in fucked_note:
    url = '------'
    title = '*******'
    try :
        url = 'www.guoku.com' + note.entity.absolute_url
        title = note.entity.title
    except Exception as e :
        pass

    nickname = '########'
    try :

       nickname =  note.user.nickname
    except:
        pass


    writer.writerow([
        note.note.encode('utf-8'),
        nickname.encode('utf-8'),
    ])




