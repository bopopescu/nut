from django.db import models
from datetime import datetime

from hashlib import md5
from apps.core.models import GKUser


class SessionKeyManager(models.Manager):
    def generate_session(self, user_id, username, email, api_key):
        _session = username + email + api_key + unicode(datetime.now())
        _session_key = md5(_session.encode('utf-8')).hexdigest()
        _session_object = self.create(
            user_id = user_id,
            app_id = 1,
            session_key = _session_key
        )
        return _session_object

    def get_user_id(self, session_key):
        _session_object = self.get(
            session_key = session_key
        )
        return _session_object.user_id


class AppsManager(models.Manager):

    def create_new_apps(self, user_id, **kwargs):
        _user = GKUser.objects.get(pk = user_id)
        _app_name = kwargs.get('app_name', None)
        _app_desc = kwargs.get('app_desc', None)
        _api_key_string = _user.username + _user.email + datetime.now().strftime('%s')
        _api_key = md5(_api_key_string.encode('utf-8')).hexdigest()
        _api_secret_string = _user.username + _user.password + _api_key
        _api_secret = md5(_api_secret_string).hexdigest()
        _apps_obj = self.create(user=_user,
                                app_name=_app_name,
                                desc=_app_desc,
                                api_key=_api_key,
                                api_secret=_api_secret)
        return _apps_obj

__author__ = 'edison'
