#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.log import getLogger
from django.utils.encoding import force_bytes
from sendcloud import address_list
from apps.core.models import SD_Address_List
from apps.core.tasks import BaseTask
from apps.core.utils.commons import verification_token_generator
from settings import GUOKU_MAIL, GUOKU_NAME


log = getLogger('django')


def send_forget_password_mail(gk_user, domain=None, template_invoke_name=None,
                              token_generator=None):
    _send_forget_password_mail.delay(gk_user=gk_user,
                                     domain=domain,
                                     template_invoke_name=template_invoke_name,
                                     token_generator=token_generator)


def send_activation_mail(gk_user):
    _send_activation_mail.delay(gk_user=gk_user)


def add_user_to_list(gk_user):
    _add_user_to_list.delay(gk_user)


def delete_user_from_list(gk_user):
    all_list = SD_Address_List.objects.all()
    for addr_list in all_list:
        sd_list = address_list.SendCloudAddressList(
            mail_list_addr=addr_list.address,
            member_addr=gk_user.email)
        if sd_list.get():
            sd_list.delete_member()


def update_user_name_from_list(gk_user):
    all_list = SD_Address_List.objects.all()
    for addr_list in all_list:
        sd_list = address_list.SendCloudAddressList(
            mail_list_addr=addr_list.address,
            member_addr=gk_user.email)
        if sd_list.get():
            sd_list.add_member(name=gk_user.nickname, upsert='true')


@task(base=BaseTask, name='add_user_to_list')
def _add_user_to_list(gk_user):
    addr_list = _get_available_list()
    sd_list = address_list.SendCloudAddressList(
        mail_list_addr=addr_list.address,
        member_addr=gk_user.email)
    sd_list.add_member(name=gk_user.nickname, upsert='true')


@task(base=BaseTask, name='send_verification_mail')
def _send_activation_mail(gk_user):
    template_invoke_name = settings.VERFICATION_EMAIL_TEMPLATE
    mail_message = EmailMessage(to=(gk_user.email,),
                                from_email=GUOKU_MAIL, )
    uidb64 = urlsafe_base64_encode(force_bytes(gk_user.id))
    token = verification_token_generator.make_token(gk_user)
    reverse_url = reverse('register_confirm',
                          kwargs={'uidb64': uidb64,
                                  'token': token})
    verify_link = "http://{0:s}{1:s}".format(settings.SITE_DOMAIN, reverse_url)
    sub_vars = {'%verify_link%': (verify_link,)}
    mail_message.template_invoke_name = template_invoke_name
    mail_message.from_name = GUOKU_NAME
    mail_message.sub_vars = sub_vars
    mail_message.send()


@task(base=BaseTask, name='send_forget_password_mail')
def _send_forget_password_mail(gk_user, domain=None, token_generator=None,
                               template_invoke_name=None):
    domain = domain or settings.SITE_DOMAIN
    template_invoke_name = template_invoke_name or settings.RESET_PASSWORD_TEMPLATE
    token_generator = token_generator or default_token_generator

    uid = urlsafe_base64_encode(force_bytes(gk_user.pk))
    token = token_generator.make_token(gk_user)
    mail_message = EmailMessage(to=(gk_user.email,),
                                from_email=GUOKU_MAIL, )
    reverse_url = reverse('web_password_reset_confirm',
                          kwargs={'uidb64': uid, 'token': token})
    reset_link = "{0:s}{1:s}".format(domain, reverse_url)
    sub_vars = {'%name%': (gk_user.nickname,),
                '%reset_link%': (reset_link,)}
    mail_message.template_invoke_name = template_invoke_name
    mail_message.sub_vars = sub_vars
    mail_message.from_name = GUOKU_NAME
    mail_message.send()


def _get_available_list():
    largest_list = SD_Address_List.objects.filter(members_count__lt=100000) \
        .order_by('-members_count')[0]
    if not largest_list:
        return _create_list()
    return largest_list


def _create_list():
    last_id = SD_Address_List.objects.order_by('-pk')[0].pk
    new_name = 'all_gkusers_%d' % (last_id + 1)
    new_list = SD_Address_List(address='%s@maillist.sendcloud.org' % new_name,
                               name=new_name,
                               description=new_name)
    new_list.save()
    return new_list
