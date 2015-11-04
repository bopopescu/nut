from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from apps.management.decorators import staff_only

from apps.core.models import Event,Event_Status
from apps.core.forms.event import EditEventForm, CreateEventForm
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from django.utils.log import getLogger
from apps.web.utils.viewtools import get_paged_list

from django.shortcuts import redirect

log = getLogger('django')


@login_required
@staff_only
def list(request, template='management/event/list.html'):

    _page = request.GET.get('page', 1)
    event_list = Event.objects.all().order_by('-slug')

    events = get_paged_list(event_list,_page,30)

    # paginator = ExtentPaginator(event_list, 30)
    #
    # try:
    #     events = paginator.page(_page)
    # except PageNotAnInteger, e:
    #     events = paginator.page(1)
    # except EmptyPage:
    #     raise Http404

    return render_to_response(
        template,
        {
            'events': events,
        },
        context_instance=RequestContext(request),
    )

@login_required
@staff_only
def create(request, template='management/event/create.html'):

    if request.method == 'POST':
        _forms = CreateEventForm(request.POST)
        if _forms.is_valid():
            _forms.save()
            return redirect('management_event')
    else:
        _forms = CreateEventForm()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance=RequestContext(request),
    )

@login_required
@staff_only
def edit(request, eid, template='management/event/edit.html'):

    try:
        event = Event.objects.get(pk=eid)
    except Event.DoesNotExist:
        raise Http404

    if not hasattr(event, 'event_status'):
        event_status = Event_Status(event=event, is_published=False, is_top=False)
        event_status.save()


    if request.method    == 'POST':
        _forms = EditEventForm(event, data=request.POST)
        if _forms.is_valid():
            _forms.save()
            return redirect('management_event')
        else:

            pass
    else:
        status = 0
        is_published = 0
        is_top = 0

        if event.status:
            status = 1
        if event.event_status.is_published:
            is_published =1
        if event.event_status.is_top:
            is_top=1

        data = {
            'title': event.title,
            'tag': event.tag,
            'toptag':event.toptag,
            'slug': event.slug,
            'status': status,
            'is_published':is_published,
            'is_top': is_top,
        }
        _forms = EditEventForm(event, initial=data)


    return render_to_response(
        template,
        {
            'event': event,
            'forms': _forms,
        },
        context_instance=RequestContext(request),
    )

__author__ = 'edison'
