from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger

from apps.core.models import Note_Comment
from apps.core.extend.paginator import ExtentPaginator, InvalidPage, EmptyPage
# from apps.core.


log = getLogger('django')


def list(request, template='management/comment/list.html'):

    page = request.GET.get('page', 1)

    comment_list = Note_Comment.objects.all()

    paginator = ExtentPaginator(comment_list, 30)


    try:
        comments = paginator.page(page)
    except InvalidPage:
        comments = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'comments': comments,
        },
        context_instance = RequestContext(request)
    )

def note_comment_list(request, note_id, template='management/notes/comment/list.html'):

    note_comment_list = Note_Comment.objects.filter(note_id = note_id)

    return render_to_response(
                        template,
                        {
                            'note_comments': note_comment_list,
                        },
                        context_instance = RequestContext(request))

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete(request, comment_id):

    try:
        comment = Note_Comment.objects.get(pk = comment_id)
    except Note_Comment.DoesNotExist:
        raise Http404
    return

__author__ = 'edison'
