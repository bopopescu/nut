from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader

from apps.core.utils.http import JSONResponse
from apps.core.models import Entity, Note, Note_Comment
from django.utils.log import getLogger

log = getLogger('django')


def entity_detail(request, entity_hash, templates='web/entity/detail.html'):
    _entity_hash = entity_hash

    _entity = Entity.objects.get(entity_hash = _entity_hash)

    log.info(_entity.category)

    return render_to_response(
        templates,
        {
            'entity': _entity,
        },
        context_instance = RequestContext(request),
    )



def entity_note_comment(request, nid, template='web/entity/note/comment_list.html'):

    _user = None
    if request.user.is_authenticated():
        _user = request.user


    _comment_list = Note_Comment.objects.filter(note_id= nid)

    log.info(_comment_list)
    _t = loader.get_template(template)
    _c = RequestContext(request, {
        'comment_list': _comment_list,
        'note_id': nid,
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
