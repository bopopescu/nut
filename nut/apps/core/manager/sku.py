from django.db import models


class SKUQuerySet(models.query.QuerySet):
    def sku_for_entity(self,entity):
        return self.filter(entity_id = entity.id)


class SKUManager(models.Manager):
    def get_queryset(self):
        return SKUQuerySet(self.model, using=self._db)

    def sku_for_entity(self, entity):
        return self.get_queryset().sku_for_entity(entity)
