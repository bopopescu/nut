# coding=utf-8
import csv
from pprint import pprint

from django.core.management.base import BaseCommand

from apps.core.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):

        articles = Article.objects.filter(related_entities__status__gte=0,
                                          related_entities__buy_links__origin_source='jd.com')

        data_list = [Command.get_data(article) for article in articles]
        pprint(data_list)
        with open('jd_article.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['article_title', 'article_url', 'publish_time', 'note_count',
                                                   'source', 'read_count', 'tags'])
            writer.writeheader()
            writer.writerows(data_list)

    @staticmethod
    def get_data(article):
        return {
            'article_title': article.title.encode('utf-8'),
            'article_url': 'http://www.guoku.com{}'.format(article.url).encode('utf-8'),
            'publish_time': article.created_datetime,
            'note_count': article.comment_count,
            'source': article.source,
            'read_count': article.read_count,
            'tags': article.tags_string.encode('utf-8')
        }
