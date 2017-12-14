from celery.task import task
import urllib2

from apps.core.utils.image import HandleImage
from apps.core.tasks import BaseTask
from apps.core.models import User_Profile, Sina_Token, Taobao_Token
from apps.core.utils.taobaoapi.user import TaobaoOpenUid

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MOGILEFS_MEDIA_URL', 'avatar/')
image_host = getattr(settings, 'IMAGE_HOST', None)

taobao_app_key = getattr(settings, 'TAOBAO_APP_KEY', None)
taobao_app_secret = getattr(settings, 'TAOBAO_APP_SECRET', None)


@task(base=BaseTask)
def fetch_avatar(avatar_url, user_id, *args, **kwargs):

    try:
        profile = User_Profile.objects.get(user_id = user_id)
    except User_Profile.DoesNotExist:
        return

    f = urllib2.urlopen(avatar_url)
    # return

    image = HandleImage(f)
    avatar_file = image.avatar_save(resize=False)
    profile.avatar = avatar_file
    profile.save()


@task(base=BaseTask)
def update_token(*args, **kwargs):

    _user_id = kwargs.pop('user_id')
    _weibo_id = kwargs.pop('weibo_id', None)
    _taobao_id = kwargs.pop('taobao_id', None)
    _screen_name = kwargs.pop('screen_name')
    _access_token = kwargs.pop('access_token')
    _expires_in = kwargs.pop('expires_in')

    if _weibo_id:
        token = Sina_Token(
            user_id = _user_id,
            sina_id = _weibo_id,
        )
        token.screen_name = _screen_name
        token.access_token = _access_token
        token.expires_in = _expires_in
        # token.save()
    else:
        token = Taobao_Token(
            user_id = _user_id,
            taobao_id = _taobao_id,
        )
        token.taobao_id = _taobao_id
        token.screen_name = _screen_name
        token.access_token = _access_token
        token.expires_in = _expires_in

        t = TaobaoOpenUid(app_key=taobao_app_key, app_secret=taobao_app_secret)
        open_uid = t.get_open_id(_taobao_id)
        if open_uid:
            token.open_uid = open_uid

    token.save()

    return token

__author__ = 'edison'
