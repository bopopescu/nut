#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mock import Mock
from apps.core.models import SD_Address_List


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
    return SD_Address_List.objects.all()
