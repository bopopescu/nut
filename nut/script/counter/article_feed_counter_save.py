import os, sys


# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Article
from apps.counter.utils.data import FeedCounterBridge


articles = Article.objects.filter(publish=Article.published)
counterBridge = FeedCounterBridge()

need_update_feed_article_id_set = counterBridge.get_need_update_article_id_set()

for id in need_update_feed_article_id_set:
    try :
        article = Article.objects.get(pk=id)
        article.feed_read_count =  counterBridge.get_article_feed_read_count(id)
        article.save(skip_updatetime=True)
    except Exception as e :
        pass

counterBridge.clear_need_update_article_id_set()

sys.exit(0)


