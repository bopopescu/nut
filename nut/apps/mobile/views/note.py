from django.views.decorators.csrf import csrf_exempt
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Entity, Note, Note_Poke, Note_Comment
from apps.core.tasks.note import post_note_task, depoke_note_task
from apps.mobile.models import Session_Key
from apps.mobile.forms.note import PostNoteForms, UpdateNoteForms
from apps.mobile.forms.comment import PostNoteCommentForm

from django.utils.log import getLogger

log = getLogger('django')


@check_sign
def detail(request, note_id):

    _key = request.GET.get('session', None)
    try:
        _session = Session_Key.objects.get(session_key = _key)
        np = Note_Poke.objects.user_poke_list(user=_session.user, note_list=[note_id])
    except Session_Key.DoesNotExist:
        np = None


    res = dict()
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    res['note'] = note.v3_toDict(user_note_pokes=np)
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


@csrf_exempt
@check_sign
def poke(request, note_id, target_status):

    res = {
        'note_id': int(note_id)
    }
    if request.method == "POST":
        _key = request.POST.get('session', None)

        try:
            _session = Session_Key.objects.get(session_key = _key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)

        if target_status == "1":
            post_note_task.delay(uid=_session.user_id, nid=note_id)
            res['poke_already'] = 1
        else:
            depoke_note_task.delay(uid=_session.user_id, nid=note_id)
            res['poke_already'] = 0
        log.info(res)
        return SuccessJsonResponse(res)

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def post_note(request, entity_id):

    if request.method == "POST":
        # _key = request.POST.get('session')
        try:
            entity = Entity.objects.get(pk = entity_id)
        except Entity.DoesNotExist:
            return ErrorJsonResponse(status=404)

        _forms = PostNoteForms(entity=entity, data=request.POST)
        if _forms.is_valid():
            res = _forms.save()
            return SuccessJsonResponse(res)
        return ErrorJsonResponse(status=403)

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def update_note(request, note_id):
    if request.method == "POST":
        _key = request.POST.get('session')
        try:
            _session = Session_Key.objects.get(session_key = _key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)

        try:
            note = Note.objects.get(pk=note_id, user=_session.user)
        except Note.DoesNotExist:
            return ErrorJsonResponse(status=404)

        _forms = UpdateNoteForms(note=note, data=request.POST)
        # log.info(request.POST)
        if _forms.is_valid():
            res = _forms.update()
            return SuccessJsonResponse(res)
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def post_comment(request, note_id):

    if request.method == "POST":
        # log.info(request.POST)
        try:
            note = Note.objects.get(pk = note_id)
        except Note.DoesNotExist:
            return ErrorJsonResponse(status=404)

        _forms = PostNoteCommentForm(note=note, data=request.POST)
        if _forms.is_valid():
            res = _forms.save()
            return SuccessJsonResponse(res)
        return ErrorJsonResponse(status=403)

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def del_comment(request, note_id, comment_id):
    if request.method == "POST":
        _key = request.POST.get('session')
        try:
            _session = Session_Key.objects.get(session_key = _key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        # log.info("comment id %s" % comment_id)
        try:
            nc = Note_Comment.objects.get(user=_session.user, pk=comment_id)
            nc.delete()
            return SuccessJsonResponse(data={'delete_already':1})
        except Note_Comment.DoesNotExist:
            return ErrorJsonResponse(status=404)
    return ErrorJsonResponse(status=400)

__author__ = 'edison7500'
