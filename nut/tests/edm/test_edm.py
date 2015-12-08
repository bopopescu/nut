#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from apps.core.models import SD_Address_List, EDM
from apps.core.tasks import add_user_to_list
from apps.core.tasks.edm import get_available_list

def test_send_edm(client, sd_address_lists, edm_robot, fixture_send_cloud_template):
    edm_robot.statues = EDM.sd_verify_succeed
    send_edm_url = reverse('send_edm', edm_id=edm_robot.pk)
    assert fixture_send_cloud_template.send_to_list.called
    response = client.get(send_edm_url)


def test_get_available_list(sd_address_lists):
    all_list = sd_address_lists.all()
    list_count = len(all_list)
    addr_list = sd_address_lists.filter(members_count__lt=100000)\
        .order_by('members_count')[0]
    get_available_list() == addr_list
    assert addr_list.members_count < 100000

    for addr_list_item in all_list:
        addr_list_item.members_count = 100000
        addr_list_item.save()

    new_list = get_available_list()
    assert new_list not in all_list
    assert SD_Address_List.objects.count() - list_count == 1
    assert new_list.members_count == 0


def test_add_user_to_list(gk_user, sd_address_lists, patch_send_cloud_address_list):
    available_list = get_available_list()
    count = available_list.members_count

    add_user_to_list(gk_user)
    assert patch_send_cloud_address_list.add_member.called
    addr_list = SD_Address_List.objects.get(pk=available_list.pk)
    assert addr_list.members_count - count == 1
