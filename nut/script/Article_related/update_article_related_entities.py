import os, sys

sys.path.append('/data/www/nut')
# for testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

from apps.core.models import Article

articles = Article.objects.filter(publish=Article.published)

for article in articles:
    article.save(skip_updatetime=True)