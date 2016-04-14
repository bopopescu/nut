import jieba.analyse
from model.article import Article
from HTMLParser import HTMLParser


#
# def strip_tags(html_string):
#     html_string = html_string.strip()
#     html_string = html_string.strip('\n')
#     res = []
#     parser = HTMLParser()
#     parser.handle_data = res.append
#     parser.feed(html_string)
#     parser.close()
#
#     return ''.join(res)

def get_textrank(article_id):

    article = Article.query.get(article_id)
    # print article
    title = jieba.analyse.textrank(article.title, topK=3, withWeight=True)
    # print title
    content = jieba.analyse.textrank(article.strip_content, topK=20, withWeight=True, allowPOS=('ns', 'n'))

    return title, content

