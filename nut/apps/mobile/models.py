from django.db import models
from django.core.cache import cache
from apps.core.models import GKUser
from apps.mobile.manager.mobile_manager import SessionKeyManager, AppsManager
from hashlib import md5

from django.utils.log import getLogger

log = getLogger('django')



class APIUser(GKUser):

    class Meta:
        proxy = True

    @property
    def fans_list(self):
        # log.info("cache cache")
        # return self.fans.all().values_list('follower_id', flat=True)
        key_string = "user_fans_%s" % self.id
        key = md5(key_string.encode('utf-8')).hexdigest()

        res = cache.get(key)
        if res:
            log.info("hit hit")
            return res
        res = super(APIUser, self).fans_list
        cache.set(key, res, timeout=3600)
        return res


    @property
    def following_list(self):
        # log.info("cache cache")
        key_string = "user_follow_%s" % self.id
        key = md5(key_string.encode('utf-8')).hexdigest()

        res = cache.get(key)
        if res:
            # log.info("hit hit")
            return res
        res = list(super(APIUser, self).following_list)
        cache.set(key, res, timeout=3600)
        return res



class Apps(models.Model):
    user = models.ForeignKey(GKUser)
    app_name = models.CharField(u'application name', max_length=30, unique=True)
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
    user = models.ForeignKey(APIUser, related_name = "mobile_client_session")
    app = models.ForeignKey(Apps)
    session_key = models.CharField(max_length = 64, unique = True, editable = False)
    create_time = models.DateTimeField(auto_now_add = True)
    objects = SessionKeyManager()

    def __unicode__(self):
        return self.session_key
    #
    # @property
    # def user(self):
    #     log.info(self.user_id)
    #     _user = APIUser.objects.get(pk = self.user_id)
    #     return _user
        # return self.user


class V3_User(GKUser):

    class Meta:
        proxy = True



__author__ = 'edison'
