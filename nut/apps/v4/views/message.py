from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Selection_Entity, Entity_Like, User_Follow, Note, \
    Note_Comment, Note_Poke, Article_Dig
# from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.v4.views import APIJsonView


from datetime import datetime
import time

from django.utils.log import getLogger
log = getLogger('django')


class MessageView(APIJsonView):

    def get_data(self, context):
        remove_user_list = []
        _messages = self.user.notifications.filter(timestamp__lt=self.timestamp).exclude(
            actor_object_id__in=remove_user_list)
        da = Article_Dig.objects.filter(user=self.user).values_list('article_id', flat=True)
        res = []
        for row in _messages[:self.count]:
            if isinstance(row.action_object, User_Follow):
                _context = {
                    'type': 'user_follow',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'follower': row.actor.v3_toDict()
                    }
                }
                res.append(_context)
            elif isinstance(row.action_object, Note):
                _context = {
                    'type': 'entity_note_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'note': row.action_object.v3_toDict(),
                        'entity': row.target.v3_toDict(),
                    }
                }
                res.append(_context)
            elif isinstance(row.action_object, Note_Poke):
                _context = {
                    'type': 'note_poke_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'note': row.target.v3_toDict(has_entity=True),
                        'poker': row.actor.v3_toDict(),
                    }
                }
                res.append(_context)
            elif isinstance(row.action_object, Note_Comment):
                _context = {
                    'type': 'note_comment_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'comment': row.action_object.v3_toDict(),
                        'note': row.target.v3_toDict(has_entity=True),
                        'comment_user': row.actor.v3_toDict(),
                    }
                }
                res.append(_context)
            elif isinstance(row.action_object, Entity_Like):
                _context = {
                    'type': 'entity_like_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'liker': row.actor.v3_toDict(),
                        'entity': row.target.v3_toDict(),
                    }
                }

                res.append(_context)
            elif isinstance(row.action_object, Selection_Entity):
                _context = {
                    'type': 'note_selection_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        # 'note' : MobileNote(_message.note_id).read(_request_user_id),
                        'note': row.target.top_note.v3_toDict(),
                        'entity': row.target.v3_toDict(),
                    }
                }
                res.append(_context)
            elif isinstance(row.action_object, Article_Dig):
                _context = {
                    'type': 'dig_article_message',
                    'created_time': time.mktime(row.timestamp.timetuple()),
                    'content': {
                        'digger': row.actor.v3_toDict(),
                        'article': row.target.v4_toDict(articles_list=da),
                    }
                }
                res.append(_context)

        self.user.notifications.mark_all_as_read()

        return res

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        # self.user = None
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.user = _session.user
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)

        self.timestamp = request.GET.get('timestamp', None)
        if self.timestamp != None:
            self.timestamp = datetime.fromtimestamp(float(self.timestamp))
        else:
            self.timestamp = datetime.now()

        self.count = int(request.GET.get('count', 10))

        return super(MessageView, self).get(request, *args, **kwargs)


__author__ = 'edison'
