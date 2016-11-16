# coding=utf-8

from apps.core.tests.models.Base import DBTestBase
from apps.core.models import Article


class ArticleModelTest(DBTestBase):
    def setUp(self):
        super(ArticleModelTest, self).setUp()
        self.article = Article.objects.create(**{
            'creator': self.the_user,
            'title':  'test',
        })

    def test_make_slug_work(self):
        self.assertEqual(self.article.make_slug(), 'test')
        article = Article.objects.get(pk=self.article.id)
        self.assertEqual(article.article_slug, 'test')


    def test_make_slug_dup(self):
        self.article2 = Article.objects.create(**{
            'creator': self.the_user,
            'title': 'test',
        })
        self.assertEqual(self.article.article_slug, 'test')
        self.assertEqual(self.article2.make_slug(), 'test1')

        self.article3 = Article.objects.create(**{
            'creator': self.the_user,
            'title': 'test'
        })

        self.assertEqual(self.article3.article_slug, 'test2')

        self.assertEqual(self.article.make_slug(), 'test')


