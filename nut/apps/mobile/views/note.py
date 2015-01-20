from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Note
from apps.mobile.models import Session_Key
from apps.core.tasks.note import post_note, depoke_note


@check_sign
def detail(request, note_id):
    res = dict()
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    res['note'] = note.v3_toDict()
    res['entity'] = note.entity.v3_toDict()
    res['poker_list'] = []
    for poker in note.pokes.all():
        res['poker_list'].append(
            poker.user.v3_toDict()
        )

    res['comment_list'] = []
    for comment in note.comments.all():
        res['comment_list'].append(comment.v3_toDict())


    return SuccessJsonResponse(res)


@check_sign
def poke(request, note_id, target_status):

    res = {
        'note_id': int(note_id)
    }
    if request.method == "POST":
        _key = request.GET.get('session', None)

        try:
            _session = Session_Key.objects.get(session_key = _key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)

        if target_status == "1":
            post_note(uid=_session.user_id, nid=note_id)
            res['poke_already'] = 1
        else:
            depoke_note(uid=_session.user_id, nid=note_id)
            res['poke_already'] = 0

        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)

__author__ = 'edison7500'
