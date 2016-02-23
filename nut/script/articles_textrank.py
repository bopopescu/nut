import os, sys
sys.path.append(os.getcwd() + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

# print os.getcwd() + '/..'
from django.utils.html import strip_tags
from apps.core.models import Selection_Article
import requests
import HTMLParser
h_parser = HTMLParser.HTMLParser()

sla = Selection_Article.objects.all()

#
for row in sla:
     content = h_parser.unescape(strip_tags(row.article.content))
     r = requests.post("http://192.168.99.100:8000/textrank", data={'text':content})
     print row.article.pk, r.json()