from django.conf.urls import url, patterns
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
from apps.core.forms.account import UserSetPasswordForm


urlpatterns = patterns(
    'apps.web.views.account',
    url(r'^three-part/register/$', 'register_from_three_part', name='web_register_from_three_part'),

    url(r'^forget/password/$', 'forget_password', name='web_forget_password'),
    url(r'^send/mail/finished/$', 'send_mail_finished', name='web_send_mail_finished'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {
            'template_name':'web/account/password_rest_confirm.html',
            'post_reset_redirect':'web_password_rest_complete',
            'set_password_form': UserSetPasswordForm,
        },
        name='web_password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete,
        {
            'template_name':'web/account/password_rest_complete.html',
        },
        name='web_password_rest_complete'),

    url(r'^send/verify/mail/$', 'send_verification_mail', name='send_verification_mail'),
    url(r'^user/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'register_mail_confirm',
        name='register_confirm')
)

__author__ = 'edison7500'
