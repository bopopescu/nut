from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView

from django.forms import ModelForm ,BooleanField

from braces.views import AjaxResponseMixin,JSONResponseMixin, UserPassesTestMixin

from apps.core.models import GKUser, Media
from apps.core.forms.user import UserForm, GuokuSetPasswordForm, AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.management.decorators import admin_only
from apps.core.serializers.users import GKUserSerializer
from apps.core.views import LoginRequiredMixin


from django.utils.log import getLogger
log = getLogger('django')

from rest_framework import generics

class RESTfulUserListView(generics.ListCreateAPIView):
        queryset = GKUser.objects.all()
        serializer_class = GKUserSerializer


class UserAuthorSetForm(ModelForm):
    isAuthor = BooleanField(required=False)
    # http://stackoverflow.com/questions/31349584/appending-formdata-field-with-value-as-a-boolean-false-causes-the-function-to-fa
    def __init__(self,*args, **kwargs):
        super(UserAuthorSetForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        _user = self.instance
        _user.setAuthor(self.cleaned_data.get('isAuthor'))

    class Meta:
        model = GKUser
        fields = ['isAuthor']


class UserAuthorSetView(UserPassesTestMixin,JSONResponseMixin, UpdateView):
    pk_url_kwarg = 'user_id'
    form_class = UserAuthorSetForm
    model = GKUser

    def form_valid(self, form):
        form.save()
        return self.render_json_response({'error': 0},status=200)

    def form_invalid(self, form):
        return self.render_json_response({'error':1, 'message':'invalid form'}, status=500)

    def test_func(self,user):
        return  user.is_admin

@login_required
@admin_only
def list(request, active='1', template="management/users/list.html"):

    page = request.GET.get('page', 1)
    # active = request.GET.get('active', '1')
    admin = request.GET.get('admin', None)
    if admin:
        user_list = GKUser.objects.admin().using('slave')
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
                                'active':None,
                                'admin':admin,
                            },
                            context_instance = RequestContext(request))

    if active == '2':
        user_list = GKUser.objects.editor().using('slave')
    elif active == '1':
        user_list = GKUser.objects.active().using('slave').order_by("-date_joined")
    elif active == '0':
        user_list = GKUser.objects.blocked().using('slave')
    # elif active == '999':
    elif active == '3':
        user_list = GKUser.objects.writer().using('slave')
    else:
        user_list = GKUser.objects.deactive().using('slave')
    # else:


    # else:
    #     user_list = GKUser.objects.all().order_by("-date_joined")

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


class MediaListView(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    template_name = "management/users/media.html"
    model = Media
    paginator_class = ExtentPaginator

    def get_queryset(self):
        media = Media.objects.filter(creator=self.user_id)
        return media

    def get(self, request, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        assert self.user_id is not None
        return super(MediaListView, self).get(request, *args, **kwargs)



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
@admin_only
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
