from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.http import JSONResponse
from apps.core.models import Note_Poke



@login_required
@csrf_exempt
def poke(request, note_id):

    if request.is_ajax():
        _user = request.user

        try:
            np = Note_Poke.objects.get(user=_user, note_id=note_id)
            np.delete()
            return JSONResponse(data={'result':'0'})
        except Note_Poke.DoesNotExist:
            np =  Note_Poke(
                user=_user,
                note_id=note_id,
            )
            np.save()
        return JSONResponse(data={'result':'1'})


__author__ = 'edison'
