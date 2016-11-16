# coding=utf-8

import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


#only need run once


from apps.core.models import Article

articles = Article.objects.all()
for article in articles:
    article.save(skip_updatetime=True)


exit(0)
