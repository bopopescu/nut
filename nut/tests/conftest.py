#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from django.core.urlresolvers import reverse
from django.test.client import Client

from apps.core.models import GKUser, User_Profile


@pytest.fixture
def gk_user(db):
    """ Create a gk user for test.
    Args:
        db: test database.
    """
    user = GKUser.objects.create_user(email='guoku_robot@robot.com',
                                      password='top_secret')
    assert user.is_active == GKUser.active

    gk_profile = User_Profile(user=user,
                              nickname='guoku_test_robot')
    gk_profile.save()
    return user


@pytest.fixture
def gk_user_removed(db):
    """ Create a gk user for test.
    Args:
        db: test database.
    """
    user = GKUser.objects.create_user(email='guoku_robot_removed@robot.com',
                                      password='top_secret',
                                      is_active=GKUser.remove)
    assert user.is_active == GKUser.remove

    gk_profile = User_Profile(user=user,
                              nickname='guoku_test_robot_removed')
    gk_profile.save()
    return user


class GuokuClient(Client):

    def gk_login(self, email, password):
        login_url = reverse("web_login")
        response = self.post(login_url, data={'email': email,
                                              'password': password})
        return response

    def gk_logout(self):
        logout_url = reverse("web_logout")
        response = self.get(logout_url)
        return response


@pytest.fixture
def guoku_client(db):
    return GuokuClient()
