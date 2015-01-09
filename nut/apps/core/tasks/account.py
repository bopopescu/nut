from celery.task import task
import urllib2

from apps.core.utils.image import HandleImage
from apps.core.tasks import BaseTask
from apps.core.models import User_Profile


from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'avatar/')
image_host = getattr(settings, 'IMAGE_HOST', None)



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

__author__ = 'edison'
