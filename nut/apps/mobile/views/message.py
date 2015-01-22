from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import User_Follow, Note_Comment
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key

from django.utils.log import getLogger
import time

log = getLogger('django')


@check_sign
def message(request):
    _key = request.GET.get('session')

    try:
        _session = Session_Key.objects.get(session_key=_key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=403)

    _messages = _session.user.notifications.read()

    # log.info(_messages)
    res = []
    for row in _messages:
        log.info(row.action_object.__class__.__name__)
        # log.info(row.actor.profile.nickname)
        if isinstance(row.action_object, User_Follow):
        #
            _context = {
                'type' : 'user_follow',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content': {
                    'follower' : row.actor.v3_toDict()
                }
            }
            res.append(_context)
        elif isinstance(row.action_object, Note_Comment):
            _context = {
                'type' : 'note_comment_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                        'comment': row.action_object.v3_toDict(),
                        'note': row.action_object.note.v3_toDict(has_entity=True),
                        'comment_user':row.actor.v3_toDict(),
                    }
            }
            res.append(_context)
    return SuccessJsonResponse(res)

__author__ = 'edison'
