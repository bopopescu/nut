from django.db import models


class ArticleManager(models.Manager):
    def get_published_by_user(self,user):
        pass

    def get_drafted_by_user(self,user):
        pass

class SelectionArticleManager(models.Manager):
    def published_until(self, until_time):
        return self.get_queryset().filter(is_published=True)


