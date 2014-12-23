from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.web.forms.user import UserSettingsForm
from apps.core.utils.http import JSONResponse
# from apps.core.utils.image import HandleImage
from apps.core.forms.user import AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.models import Entity

from django.utils.log import getLogger

log = getLogger('django')


@login_required
def settings(request, template="web/user/settings.html"):
    _user = request.user

    if request.method == 'POST':
        _profile_form = UserSettingsForm(_user, request.POST)
        if _profile_form.is_valid():
            _profile_form.save()
        # _password_form = PasswordChangeForm(request.POST, user=_user)
    else:
        data = {
            'nickname': _user.profile.nickname,
            'email': _user.email,
            'bio': _user.profile.bio,
            'location': _user.profile.location,
            'city': _user.profile.city,
            'gender': _user.profile.gender,
            'website': _user.profile.website,
        }
        # log.info(data['city'])
        _profile_form = UserSettingsForm(user=_user, initial=data)
        # _password_form = PasswordChangeForm(user=_user)

    return render_to_response(
        template,
        {
            'user':_user,
            'profile_form':_profile_form,
            # 'password_form':_password_form,
        },
        context_instance = RequestContext(request),
    )


@login_required
@csrf_exempt
def upload_avatar(request):
    _user = request.user
    if request.method == 'POST':
        # log.info(request.FILES)
        _forms = AvatarForm(_user, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
        # _file_obj = request.FILES.get('avatar_img')
        # _image = HandleImage(_file_obj)
        # # _image.resize(300, 300)
        # avatar_file_name  = _image.avatar_save()
        # _user.profile.avatar = avatar_file_name
        # _user.profile.save()
        # log.info(_user.profile.avatar_url)
            return JSONResponse(status=200, data={'avatar_url':_user.profile.avatar_url})
        log.info(_forms.errors)
    return HttpResponseNotAllowed


def index(request, user_id):


    return HttpResponseRedirect(reverse('web_user_entity_like', args=[user_id,]))


def entity_like(request, user_id, template="web/user/like.html"):


    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )



def post_note(request, user_id, template="web/user/post_note.html"):

    page = request.GET.get('page', 1)

    _user = get_user_model()._default_manager.get(pk=user_id)

    # log.info(_user.note_count)
    note_list = _user.note.all().values_list('entity_id', flat=True)
    # log.info(note_list)
    paginator = ExtentPaginator(note_list, 20)

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        raise Http404

    log.info(notes.object_list)
    _entities = Entity.objects.filter(id__in=list(notes.object_list))

    return render_to_response(
        template,
        {
            'user':_user,
            'entities': _entities,
        },
        context_instance = RequestContext(request),
    )


def fans(request, user_id, template="web/user/fans.html"):

    page = request.GET.get('page', 1)

    _user = get_user_model()._default_manager.get(pk=user_id)

    fans_list = _user.fans.all()

    paginator = ExtentPaginator(fans_list, 20)

    try:
        _fans = paginator.page(page)
    except PageNotAnInteger:
        _fans = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'user':_user,
            'fans':_fans,
        },
        context_instance = RequestContext(request),
    )


def following(request, user_id, templates="web/user/following.html"):

    page = request.GET.get('page', 1)

    _user = get_user_model()._default_manager.get(pk=user_id)

    followings_list = _user.followings.all()

    paginator = ExtentPaginator(followings_list, 20)

    try:
        _followings = paginator.page(page)
    except PageNotAnInteger:
        _followings = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        templates,
        {
            'user':_user,
            'followings':_followings,
        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison'
