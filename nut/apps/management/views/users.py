from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger
from django.contrib.auth.decorators import login_required

from apps.core.models import GKUser
from apps.core.forms.user import UserForm, GuokuSetPasswordForm, AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.management.decorators import admin_only

log = getLogger('django')

@login_required
@admin_only
def list(request, active=0, template="management/users/list.html"):

    page = request.GET.get('page', 1)
    # active = request.GET.get('active', None)
    admin = request.GET.get('admin', None)

    if active == '2':
        user_list = GKUser.objects.editor()
    elif active == '1':
        user_list = GKUser.objects.active()
    elif active == '0':
        user_list = GKUser.objects.blocked()
    elif active == '999':
        user_list = GKUser.objects.deactive()
    elif admin:
        user_list = GKUser.objects.admin()
    else:
        user_list = GKUser.objects.all()

    paginator = ExtentPaginator(user_list, 30)

    try:
        users = paginator.page(page)
    except InvalidPage:
        users = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(template,
                            {
                                'users':users,
                                'active':active,
                                'admin':admin,
                            },
                            context_instance = RequestContext(request))


@login_required
@admin_only
def edit(request, user_id, template="management/users/edit.html"):

    try:
        user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    data = {
        'user_id':user.pk,
        'email':user.email,
        'nickname': user.profile.nickname,
        'is_active':user.is_active,
        'is_admin':user.is_admin,
        'gender': user.profile.gender,
        'bio': user.profile.bio,
        'website': user.profile.website,
    }

    if request.method == 'POST':
        _forms = UserForm(user=user, data=request.POST, initial=data)
        # log.info('change %s', _forms.has_changed())
        if _forms.is_valid():
            _forms.save()

    else:
        _forms = UserForm(user=user, initial=data)

    return render_to_response(template,
                                {
                                    'user':user,
                                    'forms':_forms,
                                },
                              context_instance = RequestContext(request))


@login_required
@admin_only
def reset_password(request, user_id, template='management/users/reset_password.html'):

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = GuokuSetPasswordForm(_user, request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = GuokuSetPasswordForm(user=_user)

    return render_to_response(
        template,
        {
            'user': _user,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


@login_required
def upload_avatar(request, user_id, template='management/users/upload_avatar.html'):

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    if request.method == 'POST':

        _forms = AvatarForm(_user, request.POST, request.FILES)

        if _forms.is_valid():
            _forms.save()

    else:
        _forms = AvatarForm(_user)

    return render_to_response(
        template,
        {
            'user': _user,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


@login_required
@admin_only
def post(request, user_id, template='management/users/post.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    _entity_list = _user.entities.all()

    paginator = ExtentPaginator(_entity_list, 30)


    try:
        _entities = paginator.page(page)
    except InvalidPage:
        _entities = paginator.page(1)
    except EmptyPage:
        raise  Http404

    return render_to_response(
        template,
        {
            'user': _user,
            'entities': _entities,
            'status': status,
        },
        context_instance = RequestContext(request)
    )


@login_required
@admin_only
def notes(request, user_id, template='management/users/notes.html'):

    page = request.GET.get('page', 1)
    _status = request.GET.get('status', None)

    try:
        _user = GKUser.objects.get(pk = user_id)
    except GKUser.DoesNotExist:
        raise Http404

    if _status:
        _note_list = _user.note.filter(status=_status)
    else:
        _note_list = _user.note.all()

    paginator = ExtentPaginator(_note_list, 30)
    try:
        _notes = paginator.page(page)
    except InvalidPage:
        _notes = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'user': _user,
            'notes': _notes,
            'status': _status
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
