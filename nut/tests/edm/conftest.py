#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from mock import Mock
from apps.core.models import EDM, Article, Selection_Article


@pytest.fixture
def fixtrue_selection_articles(db, gk_user):
    for i in xrange(20):
        article = Article(
            creator=gk_user,
            title='I am robot No.%d.' % i,
            cover='image_src.jpg',
            content='I am a robot No.%d.' % i,
            publish=Article.published
        )
        article.save()

        selection_article = Selection_Article(
            article=article,
            is_published=True,
        )
        selection_article.save()

    return Selection_Article.objects


@pytest.fixture
def fixture_send_cloud_template(monkeypatch):
    sd_template = Mock()
    monkeypatch.setattr('sendcloud.address_list.SendCloudTemplate',
                        sd_template)
    return sd_template.return_value


@pytest.fixture
def edm_robot(db, fixtrue_selection_articles):
    edm = EDM(
        cover_image='imageurl.jpg',
        cover_hype_link='www.guoku.com',
        cover_description='I am a robot.',
        selection_articles=fixtrue_selection_articles.all()[:5]
    )
    edm.save()
    return edm
