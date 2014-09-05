from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Note
from apps.core.forms.note import NoteForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage

log = getLogger('django')


def list(request, template='management/notes/list.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)

    if status is None:
        note_list = Note.objects.all()
    else:
        note_list = Note.objects.filter(status = int(status))

    paginator = ExtentPaginator(note_list, 30)

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


def edit(request, note_id, template='management/notes/edit.html'):

    try:
        note = Note.objects.get(pk = note_id)
    except Note.DoesNotExist:
        raise  Http404
    _entity = note.entity

    data = {
        'note_id':note.pk,
        'creator': note.user.profile.nickname,
        'content': note.note,
        'status': note.status,
        'post_time': note.post_time,
        'updated_time': note.updated_time,
    }

    if request.method == "POST":
        _forms = NoteForm(note, request.POST, initial=data)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = NoteForm(
            note=note,
            initial=data
        )

    return render_to_response(template,
                                {
                                    'forms': _forms,
                                    'entity': _entity,
                                    'note': note,
                                },
                              context_instance = RequestContext(request))

__author__ = 'edison'
