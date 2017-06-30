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
        task_list = PublishBaidu.objects.filter(publish_time__isnull=True, is_error=False).order_by('id')[:2]
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
            token = '4484c8afa31b315ec3f21e7989e35464'

            content = unicode(soup).replace('\n', '')

            # 自定义图片处理
            cover_images = json.loads(publish_task.cover_images) if publish_task.cover_images else [article.cover_url]
            if 0 < len(cover_images) < 3:
                cover_layout = u'one'
                cover_images_json = json.dumps(cover_images[0], encoding='utf-8')
            else:
                cover_layout = u'three'
                cover_images_json = json.dumps(cover_images[:3], encoding='utf-8')

            cover_images_json = cover_images_json.encode('utf-8')
            payload = {
                'app_id': u'1555485749942141',
                'tp_src': u'guocool',
                'v': u'1.0',
                'domain': unicode(publish_task.domain),
                'origin_url': urljoin(u'http://www.guoku.com', article.url).encode('utf-8'),
                'title': publish_task.title or article.title,
                'abstract': publish_task.abstract or '',
                'content': content,
                'cover_layout': cover_layout,
                'cover_images': cover_images_json.encode('utf-8'),
                'service_type': u'1',
                'goods_info': json.dumps(goods_info).encode('utf-8'),
            }
            values = u''.join(payload[key] for key in sorted(payload.iterkeys())).encode('utf-8')
            values += token
            sign = hashlib.md5(values).hexdigest()
            payload['sign'] = sign
            try:
                response = requests.post(url, data=payload)
                result = response.json()
                publish_task.publish_time = datetime.datetime.now()
                publish_task.result = json.dumps(result)
                # publish_task.is_error = 1 if result['error'] != 0 else 0
                publish_task.save()
                print(publish_task.result)
            except Exception as e:
                print(e)
