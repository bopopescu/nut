#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from apps.tag.models import Tags


@pytest.fixture
def tag(db):
    """ Create a gk user for test.
    Args:
        db: test database.
    """
    user = Tags.objects.create_user(email='guoku_robot@robot.com',
                                      password='top_secret')
    assert user.is_active == Tags.active

    return user
