from django.db import models

# from apps.core.models import Article



class ArticleManager(models.Manager):
    def get_published_by_user(self,user):
        # publish = 2   because  Article.published = 2, user 2 to avoid circular reference
        return self.get_queryset().filter(publish=2, creator=user).order_by('-updated_datetime')

    def get_drafted_by_user(self,user):
        pass

class SelectionArticleManager(models.Manager):
    def published_until(self, until_time):
        return self.get_queryset().filter(is_published=True)


