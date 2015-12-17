#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse


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
    response = guoku_client.login(gk_user.email, 'top_secret')
    assert '/'+response.url.split('/')[-2]+'/' == reverse('web_selection')
    assert response.status_code == 302

    # visit user settings page as a guoku user.
    response = guoku_client.get(user_setting_url)
    assert response.status_code == 200


def test_logout(guoku_client):
    # logout
    response = guoku_client.logout()
    assert response.status_code == 302

    # visit user settings page as an anonymous, should be redirect.
    user_setting_url = reverse('web_user_settings')
    response = guoku_client.get(user_setting_url)
    assert response.status_code == 302
