#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse


def test_list(guoku_client):
    """ Test tag list view.
    Args:
        guoku_client:
    """
    tag_list_url = reverse("tag_list_url")
    response = guoku_client.get(tag_list_url)
    assert response.status_code == 200


def test_tag_entity_list(guoku_client):
    tag_entity_list_url = reverse('tag_name_entities_url')
    response = guoku_client.get(tag_entity_list_url)
    assert response.status_code == 200


def test_tag_hash_entity_list(guoku_client):
    tag_entity_list_url = reverse('tag_entities_url')
    response = guoku_client.get(tag_entity_list_url)
    assert response.status_code == 200
