from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView , CreateView
from django.core.urlresolvers import reverse
from django.forms import ModelForm ,BooleanField, HiddenInput

from braces.views import AjaxResponseMixin,JSONResponseMixin, UserPassesTestMixin

from apps.core.models import GKUser, Media , User_Profile , Authorized_User_Profile
from apps.core.forms.user import UserForm, GuokuSetPasswordForm, AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage
from apps.management.decorators import admin_only
from apps.core.serializers.users import GKUserSerializer
from apps.core.views import LoginRequiredMixin
from apps.core.mixins.views import SortMixin, FilterMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

from apps.management.forms.users import UserAuthorInfoForm , UserAuthorSetForm ,\
                                        UserSellerSetForm

from django.utils.log import getLogger
log = getLogger('django')

from rest_framework import generics


class RESTfulUserListView(generics.ListCreateAPIView):
        queryset = GKUser.objects.all()
        serializer_class = GKUserSerializer


class UserAuthorInfoEditView(UserPassesTestMixin, UpdateView):
    template_name = 'management/users/edit_author.html'
    form_class=UserAuthorInfoForm
    pk_url_kwarg = 'user_id'
    model = Authorized_User_Profile

    def get_pk(self):
        return self.kwargs.get(self.pk_url_kwarg, None)

    def get_object(self, queryset=None):
        pk = self.get_pk()
        try:
            profile = Authorized_User_Profile.objects.get(user__id=pk)
        except Authorized_User_Profile.DoesNotExist:
            profile = Authorized_User_Profile.objects.create(user_id=pk)
        except Authorized_User_Profile.MultipleObjectsReturned:
            # one user , one or zero Authorized_User_Profile
            raise HttpResponseBadRequest
        return profile

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('management_user_edit' , args=[self.get_pk()])

    def get_context_data(self,*args, **kwargs):
        context = super(UserAuthorInfoEditView, self).get_context_data(*args, **kwargs)
        pk = self.get_pk()
        _user = GKUser.objects.get(id=pk)
        context['current_user'] = _user
        return context

    def test_func(self, user):
        return user.is_admin


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
        return user.is_admin


class UserSellerSetView(UserPassesTestMixin, JSONResponseMixin, UpdateView):
    pk_url_kwarg = 'user_id'
    form_class = UserSellerSetForm
    model = GKUser
    def form_valid(self, form):
        form.save()
        return self.render_json_response({'error': 0},status=200)

    def form_invalid(self, form):
        return self.render_json_response({'error':1, 'message':'invalid form'}, status=500)

    def test_func(self, user):
        return user.is_admin

class SellerContextMixin(object):
    def get_user(self):
        _user_id = self.kwargs.get('user_id', None)
        _user = get_object_or_404(GKUser, pk=_user_id)
        return _user

    def get_context_data(self, **kwargs):
        context = super(SellerContextMixin, self).get_context_data()
        context['current_user'] = self.get_user()
        return context

# Start seller shop manangement

class SellerShopListView(SellerContextMixin,ListView):
    model = GKUser
    template_name = 'management/users/shop/seller_shop_list.html'
    context_object_name = 'shops'
    paginate_by = 20
    paginator_class = Jpaginator

    def get_queryset(self):
        return self.get_user().shops.all()

class SellerShopCreateView(SellerContextMixin,CreateView):
    template_name =  'management/users/shop/seller_shop_create.html'
    pass

class SellerShopUpdateView(SellerContextMixin,UpdateView):
    template_name = 'management/users/shop/seller_shop_update.html'
    pass


#Seller shop management End ======================

class UserManagementListView(FilterMixin, SortMixin, UserPassesTestMixin,ListView):
    template_name = 'management/users/list.html'
    model = GKUser
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'users'
    default_sort_params = ('date_joined' , 'desc')

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'email':
            qs = qs.filter(email__icontains=filter_value)
        elif filter_field == 'nickname':
            qs = qs.filter(profile__nickname__icontains=filter_value)
        else:
            pass

        return qs

    def getActiveStatus(self):
        return self.kwargs.get('active', '1')

    def get_queryset(self):
        querySet = super(UserManagementListView,self).get_queryset()

        active = self.getActiveStatus()

        if active == '2':
            user_list = querySet.editor().using('slave')
        elif active == '1':
            user_list = querySet.active().using('slave').order_by("-date_joined")
        elif active == '0':
            user_list = querySet.blocked().using('slave')
        # elif active == '999':
        elif active == '3':
            user_list = querySet.writer().using('slave')
        elif active == '999':
            user_list = querySet.deactive().using('slave')
        elif active == '888':
            user_list = querySet.authorized_author().using('slave')
        elif active == '777':
            user_list = querySet.admin().using('slave')
        elif active == '666':
            user_list = querySet.authorized_seller().using('slave')
        else:
            user_list= []

        return user_list

    def get_context_data(self, *args, **kwargs):
        context = super(UserManagementListView, self).get_context_data()
        context['active'] = self.getActiveStatus()
        return context

    def test_func(self, user):
        return user.is_admin


# deprecated , prepare to remove
@login_required
@admin_only
def list(request, active='1', template="management/users/list.html"):

    page = request.GET.get('page', 1)

    if active == '2':
        user_list = GKUser.objects.editor().using('slave')
    elif active == '1':
        user_list = GKUser.objects.active().using('slave').order_by("-date_joined")
    elif active == '0':
        user_list = GKUser.objects.blocked().using('slave')
    # elif active == '999':
    elif active == '3':
        user_list = GKUser.objects.writer().using('slave')
    elif active == '999':
        user_list = GKUser.objects.deactive().using('slave')
    elif active == '888':
        user_list = GKUser.objects.authorized_author().using('slave')
    elif active == '777':
        user_list = GKUser.objects.admin().using('slave')
    else:
        pass


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
                                # 'admin':admin,
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
