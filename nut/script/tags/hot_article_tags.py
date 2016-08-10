import os, sys
#
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from django.core.cache import cache
from apps.tag.models import TagsManager, TagsQueryset

def generate_hot_article_tags():
    key  = TagsManager.get_hot_article_tag_key()
    cache.set(key, TagsQueryset.hot_article_tags(), 3600*24)

generate_hot_article_tags()
sys.exit(0)