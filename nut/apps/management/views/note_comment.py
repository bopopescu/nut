from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Note_Comment

log = getLogger('django')

def list(request, note_id, template='management/notes/comment/list.html'):

    return render_to_response()


__author__ = 'edison'
