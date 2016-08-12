from apps.core.models import BaseModel, GKUser, Entity
from django.db import models


class Click_Record(BaseModel):

    referer = models.CharField(max_length=1024, null=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    user = models.ForeignKey(GKUser, related_name="click_records")
    entity = models.ForeignKey(Entity, related_name="click_records")

    class Meta:
        db_table = 'click_record'