# coding=utf-8

import os,sys
sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'



# this script is for update identity_code

# it can be run may times



from apps.core.models import Article

articles  = Article.objects.all()
for article in articles:
    if article.identity_code:
        continue
    article.identity_code = article.caculate_identity_code()
    article.save(skip_updatetime=True)

