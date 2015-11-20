from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.http import JSONResponse
from apps.core.models import Note_Poke
from apps.notifications import notify
# from apps.core.tasks.note import post_note_task, depoke_note_task



@login_required
@csrf_exempt
def poke(request, note_id):
    if request.is_ajax():
        _user = request.user

        try:
            np = Note_Poke.objects.get(user=_user, note_id=note_id)
            np.delete()
            return JSONResponse(data={'result':'0', "note_id":note_id})
        except Note_Poke.DoesNotExist:
            np =  Note_Poke(
                user=_user,
                note_id=note_id,
            )
            np.save()
            # notify.send(np.user, recipient=np.note.user, action_object=np, verb="poke note", target=np.note)
        return JSONResponse(data={'result':'1', 'note_id':note_id})
    else:
        return HttpResponseNotAllowed


__author__ = 'edison'
