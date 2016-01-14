from django.db.models import get_model
# from hashlib import md5


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

from apps.core.manager.account import GKUserManager
from apps.core.manager.entity import SelectionEntityManager
from apps.core.manager.entity import EntityLikeManager
from apps.core.manager.entity import EntityManager
from apps.core.manager.note import NoteManager, NotePokeManager
from apps.core.manager.category import SubCategoryManager
from apps.core.manager.category import CategoryManager
from apps.core.manager.comment import CommentManager
from apps.core.manager.event import ShowEventBannerManager
from apps.core.manager.article import SelectionArticleManager
from apps.core.manager.article import ArticleManager
from apps.core.manager.article import ArticleDigManager
from apps.core.manager.sidebar_banner import SidebarBannerManager


__author__ = 'edison7500'
