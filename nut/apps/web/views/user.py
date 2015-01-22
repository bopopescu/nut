from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.web.forms.user import UserSettingsForm
from apps.core.utils.http import JSONResponse
# from apps.core.utils.image import HandleImage
from apps.core.forms.user import AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.models import Entity, Entity_Like, Tag, Entity_Tag, User_Follow

from apps.notifications import notify

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
            return JSONResponse(status=200, data={'avatar_url':_user.profile.avatar_url})
        log.info(_forms.errors)
    return HttpResponseNotAllowed


@login_required
@csrf_exempt
def follow_action(request, user_id):
    _fans = request.user

    try:
        uf = User_Follow.objects.get(
            follower = _fans,
            followee_id = user_id,
        )
        raise Http404
    except User_Follow.DoesNotExist, e:
        uf = User_Follow(
            follower = _fans,
            followee_id = user_id,
        )
        uf.save()
        notify.send(_fans, recipient=uf.followee, verb=u'has followed you', action_object=uf, target=uf.followee)
    return HttpResponse(1)


@login_required
@csrf_exempt
def unfollow_action(request, user_id):

    _fans = request.user

    try:
        uf = User_Follow.objects.get(
            follower = _fans,
            followee_id = user_id,
        )
        uf.delete()
    except User_Follow.DoesNotExist, e:
        raise Http404
    return HttpResponse(0)
    # return

def index(request, user_id):
    return HttpResponseRedirect(reverse('web_user_entity_like', args=[user_id,]))


def entity_like(request, user_id, template="web/user/like.html"):

    _page = request.GET.get('page', 1)
    _user = get_user_model()._default_manager.get(pk=user_id)

    entity_like_list = Entity_Like.objects.filter(user=_user).values_list('entity_id', flat=True)

    paginator = ExtentPaginator(entity_like_list, 20)

    try:
        likes = paginator.page(_page)
    except PageNotAnInteger:
        likes = paginator.page(1)
    except EmptyPage:
        raise  Http404

    # log.info(el.object_list)

    _entities = Entity.objects.filter(pk__in=list(likes.object_list))
    # log.info(_entities.query)
    el = list()
    if request.user.is_authenticated():
        el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(likes.object_list))

    return render_to_response(
        template,
        {
            'user':_user,
            'entities':_entities,
            'el':likes,
            'user_entity_likes':el,
        },
        context_instance = RequestContext(request),
    )


def post_note(request, user_id, template="web/user/post_note.html"):

    page = request.GET.get('page', 1)

    _user = get_user_model()._default_manager.get(pk=user_id)

    # log.info(_user.note_count)
    note_list = _user.note.all().values_list('entity_id', flat=True)
    log.info(note_list)
    paginator = ExtentPaginator(note_list, 20)

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        raise Http404

    # log.info(notes.object_list)
    _entities = Entity.objects.filter(id__in=list(notes.object_list))

    el = list()
    if request.user.is_authenticated():
        # _user = request.user
        el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(notes.object_list))

    return render_to_response(
        template,
        {
            'user':_user,
            'entities': _entities,
            'notes':notes,
            'user_entity_likes': el,
        },
        context_instance = RequestContext(request),
    )


def tag(request, user_id, template="web/user/tag.html"):

    _page = request.GET.get('page', 1)

    # log.info(user_id)
    tag_list = Entity_Tag.objects.user_tags(user_id)

    # log.info(tag_list)
    paginator = ExtentPaginator(tag_list, 12)

    try:
        _tags = paginator.page(_page)
    except PageNotAnInteger:
        _tags = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'tags': _tags,
            'user_id': user_id,
        },
        context_instance = RequestContext(request),
    )


def user_tag_detail(request, user_id, tag_hash, template="web/user/tag_detail.html"):

    try:
        _tag = Tag.objects.get(tag_hash=tag_hash)
    except Tag.DoesNotExist:
        raise Http404

    _page = request.GET.get('page', 1)

    # inner_qs = Entity_Tag.objects.filter(tag=_tag)
    # log.info(e)
    inner_qs = Entity_Tag.objects.filter(tag=_tag, user_id=user_id).values_list('entity_id', flat=True)
    _entity_list = Entity.objects.filter(id__in=inner_qs, status=Entity.selection)
    # log.info(entities)
    paginator = ExtentPaginator(_entity_list, 24)

    try:
        _entities = paginator.page(_page)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'tag': _tag,
            'entities': _entities,
        },
        context_instance = RequestContext(request),
    )


def fans(request, user_id, template="web/user/fans.html"):

    page = request.GET.get('page', 1)

    _user = get_user_model()._default_manager.get(pk=user_id)

    fans_list = _user.fans.all()

    paginator = ExtentPaginator(fans_list, 12)

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
    log.info(request.user.following_list)

    followings_list = _user.followings.all()

    paginator = ExtentPaginator(followings_list, 12)

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
