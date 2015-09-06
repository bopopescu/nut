from django.db import models



class SidebarBannerQuerySet(models.query.QuerySet):
    def active_sbbanners(self):
        return self.using('slave').filter(status=2).order_by('position','-updated_time')

class SidebarBannerManager(models.Manager):
    def get_queryset(self):
        return SidebarBannerQuerySet(self.model, using=self._db)
    def active_sbbanners(self):
        return self.get_queryset().active_sbbanners()
