from django.db import models
from apps.core.models import GKUser
from apps.mobile.manager.mobile_manager import SessionKeyManager, AppsManager


class Apps(models.Model):
    user = models.ForeignKey(GKUser)
    app_name = models.CharField(u'应用名称',max_length=30, unique=True)
    desc = models.TextField()
    api_key = models.CharField(max_length=64)
    api_secret = models.CharField(max_length=32)
    created_time = models.DateTimeField(auto_now=True)
    objects = AppsManager()
    class Meta:
        ordering = ['-created_time']

    def __unicode__(self):
        # app_label = 'mobile'
        return self.app_name


class Session_Key(models.Model):
    user = models.ForeignKey(GKUser, related_name = "mobile_client_session")
    app = models.ForeignKey(Apps)
    session_key = models.CharField(max_length = 64, unique = True, editable = False)
    create_time = models.DateTimeField(auto_now_add = True)
    objects = SessionKeyManager()

    def __unicode__(self):
        return self.session_key


__author__ = 'edison'
