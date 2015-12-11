from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core.models import BaseModel, GKUser, Article

class Seller_Profile(BaseModel):
    (active,deactive) = (1,0)

    SELLER_STATUS_CHOICE=[(active, _("active")),(deactive, _("blocked"))]

    (blank ,cloth, culture, food, life) = (0,1,2,3,4)

    BUS_SECTION_CHOICE = [
        (blank, "空白"),
        (cloth, "服饰"),
        (culture,"文化"),
        (food,"美食"),
        (life,"生活")
    ]

    user = models.OneToOneField(GKUser, related_name='sellerprofile', required=False)
    shop_title = models.CharField(max_length=255, db_index=True)
    seller_name = models.CharField(max_length=255, db_index=True)
    shop_desc = models.TextField(max_length=255)
    status = models.IntegerField(choices=SELLER_STATUS_CHOICE, default=active)
    logo = models.CharField(max_length=255)
    business_section = models.IntegerField(choices=BUS_SECTION_CHOICE, default=blank)

    related_articles = models.ManyToManyField(Article, related_name='related_seller')
