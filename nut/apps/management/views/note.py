from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Note
# from apps.core.forms.entity import EntityForm

log = getLogger('django')


def list(request, template='management/notes/list.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)

    if status is None:
        note_list = Note.objects.all()
    else:
        note_list = Note.objects.filter(status = int(status))

    paginator = Paginator(note_list, 30)

    try:
        notes = paginator.page(page)
    except InvalidPage:
        notes = paginator.page(1)
    except EmptyPage:
        raise Http404



    return render_to_response(template,
                                {
                                    'notes': notes,
                                    'status': status,
                                },
                                context_instance = RequestContext(request))

__author__ = 'edison'
