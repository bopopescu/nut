from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Note
# from apps.core.forms.entity import EntityForm

log = getLogger('django')


def list(request, template=''):

    return render_to_response(

    )

__author__ = 'edison'
