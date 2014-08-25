from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Note_Comment

log = getLogger('django')


def list(request, template='management/comment/list.html'):

    comment_list = Note_Comment.objects.all()

    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request)
    )

def note_list(request, note_id, template='management/notes/comment/list.html'):

    note_comment_list = Note_Comment.objects.filter(note_id = note_id)

    return render_to_response(
                        template,
                        {
                            'note_comments': note_comment_list,
                        },
                        context_instance = RequestContext(request))


__author__ = 'edison'
