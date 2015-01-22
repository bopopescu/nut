from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth import logout as auth_logout
from django.core.files.storage import default_storage
# from django.views.decorators.http import require_GET

# from apps.core.models import Sina_Token
from apps.web.forms.account import UserSignInForm, UserPasswordResetForm, UserSignUpForm
from celery import group
from apps.core.tasks.account import fetch_avatar, update_token
# from apps.web.lib.account import sina

from django.utils.log import getLogger
log = getLogger('django')



REGISTER_TEMPLATES = {
    'register' : 'web/account/register.html',
    'register-bio' : 'web/account/register_bio.html',
}

class RegisterWizard(SessionWizardView):
    file_storage = default_storage
    def get_template_names(self):
        return [REGISTER_TEMPLATES[self.steps.current]]

    def render(self, form=None, **kwargs):
        if self.request.user.is_authenticated():
            next_url = self.request.META.get('HTTP_REFERER', reverse("web_selection"))
            return HttpResponseRedirect(next_url)
        return super(RegisterWizard, self).render(form, **kwargs)

    def done(self, form_list, **kwargs):
        signup_form = form_list[0]
        user = signup_form.save()
        bio_form = form_list[1]
        bio_form.save(user = user)
        # log.info(signup_form)

        # log.info(user.pk)

        signup_form.login(self.request, user)
        return HttpResponseRedirect(reverse('web_selection'))


def login(request, template='web/account/login.html'):

    redirect_url = request.META.get('HTTP_REFERER')
    log.info("url %s" % redirect_url)
    if redirect_url is None:
        redirect_url = reverse('web_selection')

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)

    if request.is_ajax():
        template = 'web/account/partial/ajax_login.html'


    if request.method == "POST":
        _forms = UserSignInForm(request=request, data=request.POST)
        if _forms.is_valid():
            _forms.login()
            next_url = _forms.get_next_url()
            return HttpResponseRedirect(next_url)
    else:
        _forms = UserSignInForm(request, initial={
            'next':redirect_url
        })

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request),
    )


def logout(request):
    auth_logout(request)
    request.session.set_expiry(0)
    next_url = request.META.get('HTTP_REFERER', reverse('web_selection'))
    return HttpResponseRedirect(next_url)


def forget_password(request, template='web/account/forget_password.html'):

    if request.method == 'POST':
        _forms = UserPasswordResetForm(request.POST)
        if _forms.is_valid():
            _forms.save(domain_override='guoku.com',
                        subject_template_name='web/mail/forget_password_subject.txt',
                        email_template_name='web/mail/forget_password.html',
                        from_email='hi@guoku.com')
            # print "send mail ok"
    else:
        _forms = UserPasswordResetForm()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request),
    )

# from three part

# @require_GET
def register_from_three_part(request, template="web/account/three-part-register.html"):

    if request.method == "POST":
        _forms = UserSignUpForm(request.POST)
        _avatar = request.session.get('avatar')
        _weibo_id = request.session.get('weibo_id')
        _taobao_id = request.session.get('taovao_id')
        _screen_name = request.session.get('screen_name')
        _access_token = request.session.get('access_token')
        _expires_in = request.session.get('expires_in')


        if _forms.is_valid():
            user = _forms.save()

            res = group([
                fetch_avatar.s(avatar_url=_avatar, user_id=user.pk),
                update_token.s(
                        user_id = user.pk,
                        weibo_id = _weibo_id,
                        taobao_id = _taobao_id,
                        screen_name=_screen_name,
                        access_token=_access_token,
                        expires_in=_expires_in,
                    ),
            ])
            res.delay()

            _forms.login(request, user)
            return HttpResponseRedirect(reverse('web_selection'))
    else:
        screen_name = request.session.get('screen_name', None)
        # _taobao_id = request.session.get('taobao_id', None)
        if screen_name:
            _avatar = request.session.get('avatar')


            _forms = UserSignUpForm(initial={
                'nickname': screen_name
            })
        else:
            raise

    return render_to_response(
        template,
        {
            "avatar": _avatar,
            "forms": _forms,
        },
        context_instance = RequestContext(request),
    )





__author__ = 'edison'
