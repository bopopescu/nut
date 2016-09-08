import os, sys
from apps.core.models import Article


# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'


articles = Article.objects.filter(publish=Article.published)

for article in articles:
    article.save(skip_updatetime=True)