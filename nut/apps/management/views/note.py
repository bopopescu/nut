from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger
from django.contrib.auth.decorators import login_required
from apps.core.models import Note, Entity
from apps.core.forms.note import NoteForm, CreateNoteForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.management.decorators import staff_only, staff_and_editor

log = getLogger('django')


@login_required
@staff_and_editor
def list(request, template='management/notes/list.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)

    if status is None:
        note_list = Note.objects.all().order_by("-post_time")
    else:
        note_list = Note.objects.filter(status = int(status)).order_by("-post_time")

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


@login_required
@staff_and_editor
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


@login_required
@staff_and_editor
def create(request, entity_id, template="management/notes/ajax_note_create.html"):
    template = template
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    log.info(_entity)
    if request.is_ajax():
        template = "management/notes/ajax_note_create.html"

    if request.method == "POST":
        _forms = CreateNoteForm(entity=_entity, data=request.POST)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(reverse('management_entity_edit', args=[entity_id]))
    else:
        _forms = CreateNoteForm(entity=_entity)

    return render_to_response(
        template,
        {
            'entity': _entity,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
