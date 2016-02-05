import os, sys

# #
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Article
from apps.counter.utils.data import FeedCounterBridge


counterBridge = FeedCounterBridge()
articles =  Article.objects.filter(publish=Article.published)

for article  in articles:
    article.feed_read_count = counterBridge.get_article_feed_read_count(article.pk)
    article.save(skip_updatetime=True)



sys.exit(0)


