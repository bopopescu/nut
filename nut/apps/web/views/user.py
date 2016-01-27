from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, Http404, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from apps.core.tasks import send_activation_mail
from apps.web.forms.user import UserSettingsForm, UserChangePasswordForm
from apps.core.utils.http import JSONResponse, ErrorJsonResponse
# from apps.core.utils.image import HandleImage
from apps.core.models import Note, GKUser, Category
from apps.core.forms.user import AvatarForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.models import Entity, Entity_Like, \
    User_Follow,Article,User_Profile,Selection_Article

from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.tag.models import Content_Tags
# from apps.notifications import notify
from django.views.generic import ListView, DetailView, FormView, View
from apps.core.views import LoginRequiredMixin
from hashlib import md5
from django.utils.log import getLogger

from braces.views import AjaxResponseMixin, JSONResponseMixin

from django.core.cache import cache

log = getLogger('django')


class UserSendVerifyMail(LoginRequiredMixin,AjaxResponseMixin,JSONResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        _user = request.user
        _time_key = 'user_last_verify_time:%s' % _user.id
        if not cache.get(_time_key) is None:
            data = {
                'error': 1,
                'reason': 'time too close'
            }
            return self.render_json_response(data, 400)

        try:
            if not _user.profile.email_verified:
                send_activation_mail(_user)
            else:
                pass

            data = {
                'error': 0,
                'email': request.user.email
            }
            return self.render_json_response(data)
        except Exception as e:

            data = {
                'error': 1,
                'reason': 'server error'
            }
            return self.render_json_response(data, 500)


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
            'email_verified': _user.profile.email_verified,
            # 'password_form':_password_form,
        },
        context_instance = RequestContext(request),
    )

# @login_required
# def change_password(request, template="web/user/change_password.html"):
#
#     _user = request.user
#
#     if request.method == "POST":
#         _form = UserChangePasswordForm(user=_user, data=request.POST)
#         if _form.is_valid():
#             _form.save()
#     else:
#         _form = UserChangePasswordForm(user=_user)
#
#     return render_to_response(
#         template,
#         {
#             'form':_form,
#         },
#         context_instance = RequestContext(request),
#     )


class ChangePasswdFormView(LoginRequiredMixin, FormView):
    form_class = UserChangePasswordForm
    template_name = "web/user/change_password.html"
    # success_url = reverse('web_user_change_password')

    def get_form_kwargs(self):
        kwargs = super(ChangePasswdFormView, self).get_form_kwargs()
        kwargs.update(
            {
                'user': self.request.user
            }
        )
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def bind_sns(request, template="web/user/bind_sns.html"):
    _user = request.user

    return render_to_response(
        template,
        {
            'user':_user,
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

    if request.user.id == int(user_id):
        return ErrorJsonResponse(status=403)

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

    try:
        reverse_uf = User_Follow.objects.get(
            follower_id = user_id,
            followee = _fans
        )
        # mutual following
        return JSONResponse(data={'status': 2})

    except User_Follow.DoesNotExist :
        return JSONResponse(data={'status': 1})



        # notify.send(_fans, recipient=uf.followee, verb=u'has followed you', action_object=uf, target=uf.followee)
    # return JSONResponse(data={'status':1})


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

    return JSONResponse(data={'status':0})
    # return

# def index(request, user_id):
    # return HttpResponseRedirect(reverse('web_user_entity_like', args=[user_id,]))




def tag(request, user_id, template="web/user/tag.html"):

    _page = request.GET.get('page', 1)
    _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)
    # _user = get_user_model()._default_manager.get(pk=user_id)

    tag_list = Content_Tags.objects.user_tags(user_id)

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
            'user': _user,
        },
        context_instance = RequestContext(request),
    )

def articles(request,user_id, template="web/user/user_published_articles.html"):
    _page = request.GET.get('page', 1)
    _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)
    _articles  = Article.objects.get_published_by_user(_user)
    paginator = ExtentPaginator(_articles, 12)
    try:
        _articles = paginator.page(_page)
    except PageNotAnInteger:
        _articles = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(template,
        {
            'articles':_articles,
            'user':_user
        },
         context_instance = RequestContext(request),
        )

class UserPageMixin(object):
     def get_current_category(self):
        _cid = self.kwargs.get('cid', None)
        if _cid is None:
            return None
        else:
            try:
                _category = Category.objects.get(pk=_cid)
                return _category
            except Category.DoesNotExist:
                return None

     def get_showing_user(self):
        user_id =  self.kwargs['user_id']
        _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)
        return _user

     def get_pronoun(self):
        _current_user = self.get_showing_user()
        try:
            if self.request.user == _current_user:
                return _('My')
            elif _current_user.profile.gender == User_Profile.Woman:
                return _('Hers')
            else:
                return _('His')
        except Exception as e:
            return _('His')

     def get_user_like_categories(self):
        _user = self.get_showing_user()
        return _user.entity_liked_categories



class UserDetailBase(UserPageMixin, ListView):
    '''
        abstract view for user views
    '''
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'articles'


    def get_context_data(self, **kwargs):
        context_data = super(UserDetailBase, self).get_context_data(**kwargs)
        context_data['current_user'] = self.get_showing_user()
        context_data['pronoun'] = self.get_pronoun()
        return context_data




from apps.web.forms.user import UserLikeEntityFilterForm
class UserLikeView(UserDetailBase):
    paginate_by = 28
    template_name = 'web/user/user_like.html'
    context_object_name = 'current_user_likes'
    def get_context_data(self, **kwargs):
        context_data = super(UserLikeView, self).get_context_data(**kwargs)
        context_data['entity_filter_form'] = UserLikeEntityFilterForm(initial={'entityCategory': '0', 'entityBuyLinkStatus':'3'})
        context_data['user_like_top_categories']= self.get_user_like_categories()
        context_data['current_category'] =  self.get_current_category()
        return context_data

    def get_queryset(self):
        _user = self.get_showing_user()
        _category = self.get_current_category()
        if _category is None:
            _like_list = Entity_Like.objects.filter(user=_user, entity__status__gte=Entity.freeze)
        else:
            _like_list = Entity_Like.objects.filter(user=_user, entity__status__gte=Entity.freeze)\
                                            .filter(entity__category__group=_category)

        return _like_list


class UserNoteView(UserDetailBase):
    paginate_by = 20
    template_name = 'web/user/user_note.html'
    context_object_name = 'current_user_notes'
    def get_queryset(self):
        _user = self.get_showing_user()
        _note_list = Note.objects.filter(user=_user, status__gte=0 ,entity__status__gt=Entity.remove).order_by("-post_time")
        return _note_list


class UserTagView(UserDetailBase):
    paginate_by = None
    template_name = 'web/user/user_tag.html'
    context_object_name = 'current_user_tags'
    def get_queryset(self):
        _user = self.get_showing_user()
        tag_list = Content_Tags.objects.user_tags_unique(_user)
        return tag_list


class UserPublishedArticleView(UserDetailBase):
    template_name =  'web/user/user_article.html'
    paginate_by = 12
    context_object_name = 'current_user_articles'
    def get_queryset(self):
        _user = self.get_showing_user()
        _article_list = Article.objects.get_published_by_user(_user)
        return _article_list

class UserPublishedSelectionArticleView(UserDetailBase):
    template_name =  'web/user/user_article.html'
    paginate_by = 12
    context_object_name = 'current_user_articles'
    def get_queryset(self):
        _user = self.get_showing_user()
        _selection_article_ids = Selection_Article.objects.published_by_user(_user).values_list("article__id", flat=True)
        _article_list = Article.objects.get_published_by_user(_user).filter(selections__isnull = False).filter(pk__in=list(_selection_article_ids))
        return _article_list


from apps.web.forms.user import UserArticleStatusFilterForm
class UserArticleView(UserDetailBase):
    template_name =  'web/user/user_article.html'
    paginate_by = 12
    context_object_name = 'current_user_articles'
    def get_context_data(self, **kwargs):
        context_data = super(UserArticleView, self).get_context_data(**kwargs)
        context_data['article_filter_form'] = UserArticleStatusFilterForm(initial={'articleType':'published'})
        return context_data

    def get_request_articles_status(self):
        theForm = UserArticleStatusFilterForm(self.request.GET)
        return theForm.get_cleaned_article_status()

    def get_queryset(self):
        _user = self.get_showing_user()
        article_status = self.get_request_articles_status()
        if article_status == 'published':
            _article_list = Article.objects.get_published_by_user(_user)
        elif article_status == 'draft':
            _article_list = Article.objects.get_drafted_by_user(_user)
        else :
            _selection_article_ids = Selection_Article.objects.published_by_user(_user).values_list("article__id", flat=True)
            _article_list = Article.objects.get_published_by_user(_user).filter(selections__isnull = False).filter(pk__in=list(_selection_article_ids))
        # else:
        #     _article_list = Article.objects.get_published_by_user(_user)

        return _article_list

class UserFansView(UserDetailBase):
    template_name = 'web/user/user_fans.html'
    paginate_by = 12
    context_object_name = 'current_user_fans'
    def get_queryset(self):
        _user = self.get_showing_user()
        return _user.fans.filter(follower__is_active__gte=0)


class UserFollowingsView(UserDetailBase):
    template_name = 'web/user/user_followings.html'
    paginate_by = 12
    context_object_name = 'current_user_followings'
    def get_queryset(self):
        _user = self.get_showing_user()
        return _user.followings.filter(followee__is_active__gte=0)

from apps.core.models import Authorized_User_Profile

class UserIndex(UserPageMixin, DetailView):

    # template_name = 'web/user/user_index.html'
    model = GKUser
    pk_url_kwarg = 'user_id'
    context_object_name = 'current_user'

    def get_template_names(self):
        if self._current_user.is_authorized_author:
            return 'web/user/authorized_author_index.html'
        return 'web/user/user_index.html'

    def get(self, *args, **kwargs):
        self._current_user = self.get_object()
        # this is a quick fix for  www.guoku.com/download page can not be accessed
        user_domain = self.kwargs.get('user_domain', None)
        if user_domain == 'download':
            return redirect('web_download')
        return super(UserIndex, self).get(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.get_showing_user()

    def get_showing_user_by_domain(self,domain):
        try :
            profile = Authorized_User_Profile.objects.get(personal_domain_name=domain)
        except Authorized_User_Profile.DoesNotExist as e:
            raise Http404
        except Authorized_User_Profile.MultipleObjectsReturned as e:
            raise HttpResponseServerError

        return profile.user



    def get_showing_user(self):
        user_domain = self.kwargs.get('user_domain', None)
        if user_domain is not None:
            return self.get_showing_user_by_domain(user_domain)
        else:
            return super(UserIndex, self).get_showing_user()

    def get_context_data(self,**kwargs):
        context_data = super(UserIndex, self).get_context_data(**kwargs)
        current_user = context_data['object']
        context_data['recent_likes'] = current_user.likes.all()[:12]
        context_data['recent_notes'] = current_user.note.all().filter(status__gte=0,entity__status__gt=Entity.remove).order_by("-post_time")[:6]
        # get user published selection article list

        # _article_list = Article.objects.get_published_by_user(current_user).order_by('-updated_datetime')[0:6]
        _selection_article_ids = Selection_Article.objects.published_by_user(current_user).values_list("article__id", flat=True)
        # _common_article_ids    = Article.objects.get_published_by_user(current_user).exclude(pk_in=list(_selection_article_ids)).values_list("pk",flat=True)
        _article_list = Article.objects.get_published_by_user(current_user).filter(selections__isnull = False)\
                                       .filter(pk__in=list(_selection_article_ids))[:6]

        if current_user.is_authorized_author:
            context_data['author_articles'] = Article.objects.get_published_by_user(current_user)

        context_data['articles'] = _article_list

        context_data['followings'] = current_user.followings.filter(followee__is_active__gte=0)[:7]
        context_data['fans'] = current_user.fans.filter(follower__is_active__gte=0)[:7]
        context_data['tags']= Content_Tags.objects.user_tags_unique(current_user)[0:5]
        context_data['pronoun'] = self.get_pronoun()

        context_data['user_like_top_categories']= self.get_user_like_categories()
        context_data['current_category'] =  self.get_current_category()

        return context_data

def user_tag_detail(request, user_id, tag_name, template="web/user/tag_detail.html"):

    _hash = md5(tag_name.encode('utf-8')).hexdigest()
    _page = request.GET.get('page', 1)

    inner_qs = Content_Tags.objects.filter(tag__hash=_hash, creator_id=user_id, target_content_type_id=24).values_list('target_object_id', flat=True)

    _eid_list = Note.objects.filter(pk__in=inner_qs).values_list('entity_id', flat=True)
    # print _eid_list
    _entity_list = Entity.objects.filter(pk__in=list(_eid_list))

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
            'tag': tag_name,
            'entities': _entities,
        },
        context_instance = RequestContext(request),
    )

def user_goods(request, user_id, template="web/user/goods.html"):

    _page = request.GET.get('page', 1)
    _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)
    _entity_list = Entity.objects.filter(user=_user).exclude(status=Entity.remove)
    # log.info(_entity_list)
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
            'user':_user,
            'entities': _entities,
        },
        context_instance = RequestContext(request),
    )


def fans(request, user_id, template="web/user/fans.html"):

    page = request.GET.get('page', 1)

    # _user = get_user_model()._default_manager.get(pk=user_id)
    _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)

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

    _user = get_object_or_404(get_user_model(), pk=user_id, is_active__gte = 0)
    # _user = get_user_model()._default_manager.get(pk=user_id)
    # log.info(request.user.following_list)

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
