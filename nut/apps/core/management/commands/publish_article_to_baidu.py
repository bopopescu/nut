# coding=utf-8
import hashlib
import json
from urlparse import urljoin

import datetime
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from apps.core.models import PublishBaidu, Article


class Command(BaseCommand):
    help = 'publish article to baidu'

    def handle(self, *args, **options):
        task_list = PublishBaidu.objects.filter(publish_time__isnull=True).order_by('id')[:2]
        for publish_task in task_list:
            article = Article.objects.get(pk=publish_task.article_id)

            # 处理文章内容
            soup = BeautifulSoup(article.content)
            cards = soup.find_all(class_='guoku-card')
            entity_hash_list = [card['data_entity_hash'] for card in cards]
            for index, card in enumerate(cards):
                new_tag = soup.new_tag(u'iframe')
                new_tag['class'] = 'spd-faked-goods'
                new_tag['data-pos'] = index
                card.replace_with(new_tag)

            # 商品信息字段
            goods_info = [{'sku_id': entity_hash, 'tpl_id': 'BdrainrwSpdGoodsHasPic'} for entity_hash in
                          entity_hash_list]

            url = u'http://sfc.baidu.com/business/article_publish'
            token = u'4484c8afa31b315ec3f21e7989e35464'

            content = unicode(soup).replace('\n', '')

            payload = {
                'app_id': u'1555485749942141',
                'tp_src': u'guocool',
                'v': u'1.0',
                'domain': unicode(publish_task.domain),
                'origin_url': urljoin(u'http://www.guoku.com', article.url).encode('utf-8'),
                'title': publish_task.title or article.title,
                'abstract': publish_task.abstract or '',
                'content': content,
                'cover_layout': u'one',
                'cover_images': json.dumps([article.cover_url]).encode('utf-8'),
                'service_type': u'1',
                'goods_info': json.dumps(goods_info).encode('utf-8'),
            }
            values = u''.join(payload[key] for key in sorted(payload.iterkeys()))
            values += token
            sign = hashlib.md5(values.encode('utf-8')).hexdigest()
            payload['sign'] = sign

            try:
                response = requests.post(url, data=payload)
                result = response.json()
                if result['errno'] == 0:
                    publish_task.publish_time = datetime.datetime.now()
                    publish_task.save()
                    self.stdout.write(json.dumps(result))
                else:
                    self.stderr.write(json.dumps(result))
            except Exception as e:
                self.stderr.write(e)
