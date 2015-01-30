from django.db.models import get_model
from hashlib import md5



def get_entity_model():
    entity_model = get_model('core', 'Entity')
    return entity_model

def get_entity_like_model():
    entity_model = get_model('core', 'Entity_Like')
    return entity_model

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


__author__ = 'edison7500'
