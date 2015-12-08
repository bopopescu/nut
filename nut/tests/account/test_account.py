#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.core import mail
from apps.core.models import GKUser, User_Profile
from apps.core.tasks import send_activation_mail
from apps.core.tasks import send_forget_password_mail
from settings import GUOKU_MAIL


def test_register(guoku_client, gk_user):
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == gk_user.email
    assert mail.outbox[0].from_email == GUOKU_MAIL
    wizard_url = reverse('web_register')

    guoku_client.gk_login(gk_user.email, 'top_secret')
    response = guoku_client.get(wizard_url)
    assert response.status_code == 302

    guoku_client.gk_logout()
    response = guoku_client.get(wizard_url)
    assert response.status_code == 200

    email = 'guoku_robot_owl@guoku-robot.com'
    wizard_step_1_data = {
        'register-email': [email],
        'register-nickname': [u'guoku_robot_owl'],
        'register-confirm_password': [u'top_secret'],
        'register-agree_tos': [u'on'],
        'register_wizard-current_step': [u'register'],
        'register-password': [u'top_secret']
    }
    response = guoku_client.post(wizard_url, data=wizard_step_1_data)
    assert response.status_code == 200

    wizard_step_2_data = {
        u'register-bio-bio': [u'I am a robot.'],
        u'register_wizard-current_step': [u'register-bio'],
    }
    response = guoku_client.post(wizard_url, data=wizard_step_2_data)
    assert response.status_code == 302
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to[0] == email
    assert mail.outbox[1].from_email == GUOKU_MAIL


def test_login(guoku_client, gk_user):
    """ Test login view
    Args:
        guoku_client:
        gk_user:
    """
    # visit user settings page as an anonymous, should be redirect.
    user_setting_url = reverse('web_user_settings')
    response = guoku_client.get(user_setting_url)
    assert response.status_code == 302

    login_url = reverse('web_login')
    response = guoku_client.get(login_url)
    assert response.status_code == 200

    # login
    response = guoku_client.gk_login(gk_user.email, 'top_secret')
    assert '/' + response.url.split('/')[-2] + '/' == reverse('web_selection')
    assert response.status_code == 302

    # visit user settings page as a guoku user.
    response = guoku_client.get(user_setting_url)
    assert response.status_code == 200


def test_recovery_password_view(client, gk_user, gk_user_removed):
    from apps.core.forms.account import UserPasswordResetForm
    # A normal gk user.
    test_recovery_form = UserPasswordResetForm(data={'email': gk_user.email})
    assert test_recovery_form.is_valid() != False

    # A removed user can't recovery password.
    test_recovery_form = UserPasswordResetForm(
        data={'email': gk_user_removed.email})
    assert test_recovery_form.is_valid() == False

    response = client.post(reverse('web_forget_password'), data={
        'email': gk_user_removed.email
    })
    assert response.status_code == 200
    content = BeautifulSoup(response.content)
    assert content.find_all('span', attrs={'class': 'help-block'})

    response = client.post(reverse('web_forget_password'), data={
        'email': gk_user.email
    })
    assert response.status_code == 302


def test_send_recover_password_mail(gk_user):
    send_forget_password_mail(gk_user)
    assert len(mail.outbox) > 0
    assert mail.outbox[0].to[0] == gk_user.email
    assert mail.outbox[0].from_email == GUOKU_MAIL


def test_send_activation_mail(gk_user):
    send_activation_mail(gk_user)
    assert len(mail.outbox) > 0
    assert mail.outbox[0].to[0] == gk_user.email
    assert mail.outbox[0].from_email == GUOKU_MAIL


def test_email_change_signal(db, sd_address_lists, patch_send_cloud_address_list):
    """ Test email_change_signal of User_Profile:
        When a user registers, should send an activation email;
        When a user updates nickname, updates name in a address list;
        When a user updates email address, deletes this email in a address list,
        Then send an activation email.
    """
    new_guy = GKUser.objects.create_user(email='guoku_robot_new_guy@guoku-robot.com',
                                         password='top_secret')
    gk_profile = User_Profile(user=new_guy,
                              nickname='guoku_test_robot_new_guy')

    gk_profile.save()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == new_guy.email
    assert mail.outbox[0].from_email == GUOKU_MAIL

    patch_send_cloud_address_list.get.return_value = send_cloud_get_member_success_result
    gk_profile.nickname = 'guoku_test_robot_new_guy_has_new_name'
    gk_profile.save()
    assert patch_send_cloud_address_list.get.called
    assert patch_send_cloud_address_list.add_member.called

    patch_send_cloud_address_list.reset_mock()
    patch_send_cloud_address_list.get.return_value = None
    gk_profile.nickname = 'guoku_test_robot_new_guy'
    gk_profile.save()
    assert patch_send_cloud_address_list.get.called
    assert patch_send_cloud_address_list.add_member.called is False

    patch_send_cloud_address_list.reset_mock()
    patch_send_cloud_address_list.get.return_value = None
    gk_profile.user.email = 'guoku_robot_new_guy_has_new_email@guoku-robot.com'
    gk_profile.user.save()
    assert patch_send_cloud_address_list.get.called
    assert patch_send_cloud_address_list.delete_member.called is False
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to[0] == new_guy.email
    assert mail.outbox[1].from_email == GUOKU_MAIL

    patch_send_cloud_address_list.reset_mock()
    patch_send_cloud_address_list.get.return_value = send_cloud_get_member_success_result
    gk_profile.user.email = 'guoku_robot_new_guy@guoku-robot.com'
    gk_profile.user.save()
    assert patch_send_cloud_address_list.get.called
    assert patch_send_cloud_address_list.delete_member.called
    assert len(mail.outbox) == 3
    assert mail.outbox[2].to[0] == new_guy.email
    assert mail.outbox[2].from_email == GUOKU_MAIL

    assert gk_profile.email_verified == False


def test_change_password(guoku_client):
    pass


def test_logout(guoku_client):
    # logout
    response = guoku_client.gk_logout()
    assert response.status_code == 302

    # visit user settings page as an anonymous, should be redirect.
    user_setting_url = reverse('web_user_settings')
    response = guoku_client.get(user_setting_url)
    assert response.status_code == 302


send_cloud_get_member_success_result = {
  "statusCode": 200,
  "message": u"请求成功",
  "result": 'true',
  "info": {
    "dataList": [
      {
        "gmtCreated": "2015-04-30 11:15:43",
        "gmtUpdated": "2015-04-30 11:15:43",
        "address": "fake_info",
        "member": "fake@fake.com",
        "vars": ""
      }
    ],
    "count": 1
  }
}
