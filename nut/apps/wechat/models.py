from django.db import models
from django.conf import settings


class RobotDic(models.Model):
    """
        model for keyword and response dictionary
    """
    keyword = models.CharField(unique=True, max_length=128)
    resp = models.CharField(max_length=1024)
    status = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "<input keyword {0} response {1}>".format(self.keyword, self.resp)


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='wechat')
    open_id = models.CharField(max_length=255)
    joined_datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return self.open_id
