import os, sys
#
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.models import Article
from apps.counter.utils.data import RedisCounterMachine

articles = Article.objects.filter(publish=Article.published)
count_list = RedisCounterMachine.get_read_counts(articles)

for pk, read_count in count_list.iteritems():
    article = Article.objects.get(pk=pk)
    article.read_count = read_count
    article.save(skip_updatetime=True)

sys.exit(0)