from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.mobile.lib.sign import check_sign
from apps.core.models import Note



@check_sign
def detail(request, note_id):

    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        raise ErrorJsonResponse(status=404)

    res = note.v3_toDict()

    return SuccessJsonResponse(res)



__author__ = 'edison7500'
