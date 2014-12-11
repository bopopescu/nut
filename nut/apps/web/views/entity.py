from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader

from apps.core.utils.http import JSONResponse
from apps.core.models import Entity,Entity_Like, Note, Note_Comment
from apps.web.forms.comment import CommentForm
from django.utils.log import getLogger

log = getLogger('django')



def entity_detail(request, entity_hash, templates='web/entity/detail.html'):
    _entity_hash = entity_hash

    _user = None
    if request.user.is_authenticated():
        _user = request.user
    like_status = 0


    _entity = Entity.objects.get(entity_hash = _entity_hash)

    try:
        _entity.likes.get(user = _user)
        like_status = 1
    except Entity_Like.DoesNotExist:
        pass

    log.info(_entity.category)

    return render_to_response(
        templates,
        {
            'entity': _entity,
            'like_status': like_status,
        },
        context_instance = RequestContext(request),
    )



def entity_note_comment(request, nid, template='web/entity/note/comment_list.html'):

    _user = None
    if request.user.is_authenticated():
        _user = request.user


    if request.method == "POST":
        try:
            note = Note.objects.get(pk = nid)
        except Note.DoesNotExist:
            raise Http404
        _forms = CommentForm(note=note, user=_user,  data=request.POST)
        if _forms.is_valid():
            # log.info("ok ok ok ok")

            comment = _forms.save()
            template = 'web/entity/note/comment.html'

            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'comment': comment,
            })

            _data = _t.render(_c)

            return JSONResponse(
                data={
                    'data': _data,
                },
                content_type='text/html; charset=utf-8',
            )
         # log.info(_forms.errors)
        # return
    else:
        _forms = CommentForm()

    _comment_list = Note_Comment.objects.filter(note_id= nid)

    log.info(_comment_list)
    _t = loader.get_template(template)
    _c = RequestContext(request, {
        'comment_list': _comment_list,
        'note_id': nid,
        'forms': _forms
        # 'note_context': _note_context,
    })
    _data = _t.render(_c)

    return JSONResponse(
        data={
            'data':_data,
        },
        content_type='text/html; charset=utf-8',
    )


__author__ = 'edison'
