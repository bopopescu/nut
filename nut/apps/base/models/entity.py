from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..models import BaseModel


class Entity(BaseModel):

    (freeze, hide, show) = range(0, 3)
    ENTITY_STATUS_CHOICES = [
        (freeze, _("freeze")),
        (hide, _("hide")),
        (show, _("show")),
    ]

    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    creator_id = models.IntegerField(default=None, null=True, db_index=True)
    # category = models.ForeignKey(Category)
    # neo_category = models.ForeignKey(Neo_Category)
    brand = models.CharField(max_length=256, null=False, default='')
    title = models.CharField(max_length=256, null=False, default='')
    intro = models.TextField(null=False, default='')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)
    # like_count = models.IntegerField(default=0, db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    chief_image = models.CharField(max_length=64)
    detail_images = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    novus_time = models.DateTimeField(db_index=True)
    weight = models.IntegerField(default=0, db_index=True)
    rank_score = models.IntegerField(choices=ENTITY_STATUS_CHOICES, default=0)

    # objects = EntityManager()

    # search = SphinxSearch(
    #     index='entities',
    #     weights={
    #         'title': 20,
    #         'brand': 10,
    #         'intro': 5,
    #     },
    #     mode='SPH_MATCH_ALL',
    #     rankmode='SPH_RANK_NONE',
    # )

    @property
    def like_count(self):
        return self.entity_like_set.count()

    class Meta:
        ordering = ['-created_time']

    def get_absolute_url(self):
        return "/detail/%s" % self.entity_hash

    def __unicode__(self):
        return self.title




__author__ = 'edison7500'
