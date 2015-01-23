from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Note
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.notifications.models import Notification

from django.contrib.contenttypes.models import ContentType
from django.utils.log import getLogger


log = getLogger('django')


@check_sign
def activity(request):

    # log.info(request.GET)

    _key = request.GET.get('session', None)

    try:
        _session = Session_Key.objects.get(session_key = _key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=403)

    note_model = ContentType.objects.get_for_model(Note)
    # log.info(type(note_model))

    feeds = Notification.objects.filter(actor_object_id__in=_session.user.following_list, action_object_content_type=note_model)

    # log.info(feeds)

    res = []
    for row in feeds:
        res.append(
            {
                'type': 'entity',
                'content' : {
                    'entity' : row.target.v3_toDict(),
                    'note' : row.action_object.v3_toDict(),
                }
            }
        )

    return SuccessJsonResponse(res)

__author__ = 'edison'
