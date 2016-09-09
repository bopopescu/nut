import os, sys
#
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


from apps.core.models import Article
from apps.counter.utils.data import RedisCounterMachine


article_ids = list(RedisCounterMachine.get_need_update_article_id_set())

# articles = Article.objects.filter(publish=Article.published)
articles = Article.objects.filter(publish=Article.published, pk__in=article_ids)
count_list = RedisCounterMachine.get_read_counts(articles)

for pk, read_count in count_list.iteritems():
    article = Article.objects.get(pk=pk)
    article.read_count = read_count
    article.save(skip_updatetime=True)

RedisCounterMachine.clear_need_update_article_id()

sys.exit(0)
