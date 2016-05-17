import jieba.analyse
from model.article import Article
from werkzeug.contrib.cache import FileSystemCache
# from HTMLParser import HTMLParser

cache = FileSystemCache(cache_dir='/tmp/text_cache/')


def get_textrank(article_id):

    article = Article.query.get(article_id)
    # print article
    try:
        title = jieba.analyse.textrank(article.title, topK=3, withWeight=True,
                                       allowPOS=('nz', 'ns', 'vn', 'an', 'n'))
    except :
        return None, None
    # print title

    key = "article:{0}".format(article_id)
    # content = cache.get(key)
    content = None
    if content is None:
        content = jieba.analyse.textrank(article.strip_content, topK=10, withWeight=True,
                                     allowPOS=('nz', 'ns', 'vn', 'an', 'n'))
        cache.set(key, content, timeout=86400)

    return title, content

