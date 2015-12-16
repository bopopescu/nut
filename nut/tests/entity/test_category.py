#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def test_category_entities(client, db):
    web_category_list_url = reverse('web_category_list')
    response = client.get(web_category_list_url)
    assert response.status_code == 200

    web_category_list_url = reverse('web_category_list', kwargs={'order_by':'olike'})
    response = client.get(web_category_list_url)
    assert response.status_code == 200
