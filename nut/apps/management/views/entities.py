from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Entity
from apps.core.forms.entity import EntityForm

log = getLogger('django')


def list(request, template = 'management/entities/list.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)
    if status is None:
        entity_list  = Entity.objects.all()
    else:
        entity_list = Entity.objects.filter(status = int(status))

    paginator = Paginator(entity_list, 30)

    try:
        entities = paginator.page(page)
    except InvalidPage:
        entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    # log.info(paginator.page_range)
    return render_to_response(template,
                            {
                                'entities': entities,
                                'page_range': paginator.page_range[int(page) - 1: 9 + int(page)],
                                'status': status,
                            },
                            context_instance = RequestContext(request))


def edit(request, entity_id,  template='management/entities/edit.html'):

    _update = None
    try:
        entity = Entity.objects.get(pk = entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EntityForm(request.POST)
        _update = 1

        if _forms.is_valid():
            _forms.save()
            _update = 0

    else:
        _forms = EntityForm(
        initial={
            'id':entity.pk,
            'creator':entity.user.profile.nickname,
            'brand':entity.brand,
            'title':entity.title,
            'price':entity.price,
            'status': entity.status,
        }
    )

    return render_to_response(template,
                        {
                            'entity': entity,
                            'forms': _forms,
                            'update': _update,
                        },
                        context_instance = RequestContext(request))


__author__ = 'edison7500'
