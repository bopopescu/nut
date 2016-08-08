# -*- coding: utf-8 -*-

from flask_restful import reqparse, abort, Resource
from werkzeug.contrib.cache import FileSystemCache
import jieba.analyse

from applications.models.article import Article

cache = FileSystemCache(cache_dir='/tmp/text_cache/')

class ArticleTextRank(Resource):

    def get(self, article_id):
        article = Article.query.get_or_404(article_id)
        try:
            title = jieba.analyse.textrank(article.title, topK=3, withWeight=True,
                                           allowPOS=('nz', 'ns', 'vn', 'an', 'n'))
        except Exception:
            title = None
            # return None, None

        key = "article:{0}".format(article_id)
        content = cache.get(key)

        if content is None:
            content = jieba.analyse.textrank(article.strip_content, topK=10, withWeight=True,
                                             allowPOS=('nz', 'ns', 'vn', 'an', 'n'))
            cache.set(key, content, timeout=86400)

        res = {
            'title': title,
            'content': content
        }

        return res, 200

