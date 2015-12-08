#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mock import Mock
from django.core.urlresolvers import reverse
from django.test.client import Client
from apps.core.models import SD_Address_List
from apps.core.models import GKUser, User_Profile


@pytest.fixture
def gk_user(db):
    """ Create a gk user for test.
    Args:
        db: test database.
    """
    user = GKUser.objects.create_user(email='guoku_robot@guoku-robot.com',
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
    user = GKUser.objects.create_user(email='guoku_robot_removed@guoku-robot.com',
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


@pytest.fixture
def patch_send_cloud_address_list(monkeypatch):
    sd_address_list = Mock()
    monkeypatch.setattr('sendcloud.address_list.SendCloudAddressList',
                        sd_address_list)
    return sd_address_list.return_value


@pytest.fixture
def sd_address_lists(db):
    for i in xrange(5):
        sd_name = 'test_%d' % i
        sd_list = SD_Address_List(
            address='%s@sd_test.com' % sd_name,
            name=sd_name,
            description=sd_name,
            members_count=i * 20000
        )
        sd_list.save()
    return SD_Address_List.objects
