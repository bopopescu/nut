#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.core import mail

from apps.core.models import email_change_signal
from apps.core.tasks import send_activation_mail
from apps.core.tasks import send_forget_password_mail
from settings import GUOKU_MAIL


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


def test_send_recover_password_mail(client, gk_user):
    send_forget_password_mail(gk_user)
    assert len(mail.outbox) > 0
    assert mail.outbox[0].to[0] == gk_user.email
    assert mail.outbox[0].from_email == GUOKU_MAIL


def test_send_activation_mail(client, gk_user):
    send_activation_mail(gk_user)
    assert len(mail.outbox) > 0
    assert mail.outbox[0].to[0] == gk_user.email
    assert mail.outbox[0].from_email == GUOKU_MAIL


def test_email_change_signal(client):
    # create a new user profile
    #
    # when session.commit:
    #     assert mail.outbox[0]
    #
    # change;
    # check outbox;
    pass


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
