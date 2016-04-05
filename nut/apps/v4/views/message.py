from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Selection_Entity, Entity_Like, User_Follow, Note, Note_Comment, Note_Poke, Article_Dig
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key


from datetime import datetime
import time

from django.utils.log import getLogger
log = getLogger('django')


@check_sign
def message(request):
    _key = request.GET.get('session')

    _timestamp = request.GET.get('timestamp', None)
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    else:
        _timestamp = datetime.now()

    _count = int(request.GET.get('count', 10))

    try:
        _session = Session_Key.objects.get(session_key=_key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=403)

    remove_user_list = []
    # remove_user_list = V3_User.objects.deactive_user_list()
    # log.info(remove_user_list)
    # actor_object_id
    #
    # log.info(request.GET)
    _messages = _session.user.notifications.filter(timestamp__lt=_timestamp).exclude(actor_object_id__in=remove_user_list)


    # log.info(_messages.query)
    res = []
    for row in _messages[:_count]:
        # log.info(row.action_object.__class__.__name__)
        # log.info(row.actor.profile.nickname)
        if isinstance(row.action_object, User_Follow):
            _context = {
                'type' : 'user_follow',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content': {
                    'follower' : row.actor.v3_toDict()
                }
            }
            res.append(_context)
        elif isinstance(row.action_object, Note):
            _context = {
                'type' : 'entity_note_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                    'note' : row.action_object.v3_toDict(),
                    'entity' : row.target.v3_toDict(),
                }
            }
            res.append(_context)
        elif isinstance(row.action_object, Note_Poke):
            _context = {
                'type' : 'note_poke_message',
                        'created_time' : time.mktime(row.timestamp.timetuple()),
                        'content' : {
                            'note' : row.target.v3_toDict(has_entity=True),
                            'poker' : row.actor.v3_toDict(),
                        }
            }
            res.append(_context)
        elif isinstance(row.action_object, Note_Comment):
            _context = {
                'type' : 'note_comment_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                        'comment': row.action_object.v3_toDict(),
                        'note': row.target.v3_toDict(has_entity=True),
                        'comment_user':row.actor.v3_toDict(),
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
        elif isinstance(row.action_object, Selection_Entity):
            _context = {
                'type' : 'note_selection_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                    # 'note' : MobileNote(_message.note_id).read(_request_user_id),
                    'note': row.target.top_note.v3_toDict(),
                    'entity' : row.target.v3_toDict(),
                }
            }
            res.append(_context)
        elif isinstance(row.action_object, Article_Dig):
            _context = {
                'type' : 'article_dig_message',
                'created_time' : time.mktime(row.timestamp.timetuple()),
                'content' : {
                    'liker' : row.actor.v3_toDict(),
                    'article' : row.target.toDict(),
                }
            }
            res.append(_context)
    _session.user.notifications.mark_all_as_read()
    return SuccessJsonResponse(res)

__author__ = 'edison'
