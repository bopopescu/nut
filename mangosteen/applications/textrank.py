import jieba.analyse
from model.article import Article
# from HTMLParser import HTMLParser



def get_textrank(article_id):

    article = Article.query.get(article_id)
    # print article
    try:
        title = jieba.analyse.textrank(article.title, topK=3, withWeight=True)
    except :
        return None, None
    # print title
    content = jieba.analyse.textrank(article.strip_content, topK=10, withWeight=True, allowPOS=('nz', 'ns', 'vn', 'an', 'n'))

    return title, content

