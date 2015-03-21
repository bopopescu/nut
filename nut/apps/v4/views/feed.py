from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Note, Entity_Like, User_Follow
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.notifications.models import Notification


from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.utils.log import getLogger
import time

log = getLogger('django')


@check_sign
def activity(request):

    log.info(request.GET)
    _timestamp = request.GET.get('timestamp', None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _offset = int(request.GET.get('offset', '0'))
    _count = int(request.GET.get('count', '30'))
    _key = request.GET.get('session', None)

    _offset = _offset / _count + 1

    try:
        _session = Session_Key.objects.get(session_key = _key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=403)

    note_model = ContentType.objects.get_for_model(Note)
    entity_list_models = ContentType.objects.get_for_model(Entity_Like)
    user_follow = ContentType.objects.get_for_model(User_Follow)
    # log.info(entity_list_models)

    # log.info(dir(_session))
    # feed_list = Notification.objects.filter(actor_object_id__in=_session.user.following_list, action_object_content_type=note_model, timestamp__lte=_timestamp)
    feed_list = Notification.objects.filter(actor_object_id__in=_session.user.following_list,
                                            action_object_content_type__in=[note_model, entity_list_models, user_follow],
                                            timestamp__lt=_timestamp)

    # log.info(feed_list.query)

    paginator = ExtentPaginator(feed_list, _count)
    try:
        feeds = paginator.page(_offset)
    except PageNotAnInteger:
        feeds = paginator.page(1)
    except EmptyPage:
        return ErrorJsonResponse(status=404)

    # log.info(feeds)

    res = []
    for row in feeds.object_list:
        if row.action_object is None:
            continue

        log.info(row.action_object_content_type)
        if isinstance(row.action_object, Note):
            res.append(
                {
                    'type': 'entity',
                    'content' : {
                        'entity' : row.target.v3_toDict(),
                        'note' : row.action_object.v3_toDict(),
                    }
                }
            )
        elif isinstance(row.action_object, User_Follow):
            _context = {
                'type' : 'user_follow',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content': {
                    'follower' : row.actor.v3_toDict()
                }
            }
            res.append(_context)
        elif isinstance(row.action_object, Entity_Like):
            _context = {
                'type' : 'entity_like_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                    'liker' : row.actor.v3_toDict(),
                    'entity' : row.target.v3_toDict(),
                }
            }
            res.append(_context)
    return SuccessJsonResponse(res)

__author__ = 'edison'
