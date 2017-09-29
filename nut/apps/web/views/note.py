# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from apps.core.models import Note_Poke
from apps.core.utils.http import JSONResponse


@login_required
@csrf_exempt
def poke(request, note_id):
    if request.is_ajax():
        _user = request.user

        try:
            np = Note_Poke.objects.get(user=_user, note_id=note_id)
            np.delete()
            return JSONResponse(data={'result': '0', "note_id": note_id})
        except Note_Poke.DoesNotExist:
            np = Note_Poke(
                user=_user,
                note_id=note_id,
            )
            np.save()
        return JSONResponse(data={'result': '1', 'note_id': note_id})
    else:
        return HttpResponseNotAllowed
