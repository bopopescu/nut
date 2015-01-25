from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from apps.core.models import Show_Event_Banner, Event_Banner
from apps.management.forms.event_banner import CreateEventBannerForms, EditEventBannerForms
# from utils.authority import staff_only

from django.utils.log import getLogger


log = getLogger('django')


@login_required
# @staff_only
def list(request, template='management/event_banner/list.html'):

    # _show_banners = Show_Event_Banner.objects.all()
    _event_banners = Event_Banner.objects.all()
    return render_to_response(
        template,
        {
            # 'show_banners':_show_banners,
            'event_banners': _event_banners,
        },
        context_instance=RequestContext(request)
    )


@login_required
# @staff_only
def show_list(request, sid, template='management/event_banner/show_list.html'):
    _show_banners = Show_Event_Banner.objects.filter(event=sid)

    return render_to_response(
        template,
        {
            'event': sid,
            'show_banners':_show_banners,
        },
        context_instance=RequestContext(request)
    )

@login_required
# @staff_only
def create(request, event_id = None, template='management/event_banner/create.html'):
    _event_id = event_id


    if request.method == "POST":
        _forms = CreateEventBannerForms(request.POST, request.FILES)
        if _forms.is_valid():
            _event_banner = _forms.save()
            return HttpResponseRedirect(reverse('management_event_banner_edit', args=[_event_banner.id]))
    else:
        _forms = CreateEventBannerForms(initial={
            'event': _event_id,
        })

    return render_to_response(
        template,
        {
            'forms':_forms,
        },
        context_instance=RequestContext(request)
    )


@login_required
# @staff_only
def edit(request, event_banner_id, template='management/event_banner/edit.html'):

    try:
        _event_banner = Event_Banner.objects.get(pk = event_banner_id)
    except Event_Banner.DoesNotExist:
        raise Http404

    # log.info("user id %s" % _event_banner.user_id)
    try:
        show = Show_Event_Banner.objects.get(banner = _event_banner)
        event_id = show.event_id
    except Show_Event_Banner.DoesNotExist, e:
        log.error("Error %s" % e.message)
        event_id = None

    data = {
        # 'content_type': _banner.content_type,
        # 'key': _banner.key,

        # 'event_banner':_event_banner,
        'link': _event_banner.link,
        'position':_event_banner.position,
        'banner_type':_event_banner.banner_type,
        'user_id':_event_banner.user_id,
        'event': event_id,
    }

    if request.method == "POST":
        _forms = EditEventBannerForms(_event_banner, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EditEventBannerForms(_event_banner, data=data)


    return render_to_response(
        template,
        {
            'event_banner':_event_banner,
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )

__author__ = 'edison'
