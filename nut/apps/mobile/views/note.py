from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Note



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
    return SuccessJsonResponse(res)



__author__ = 'edison7500'
