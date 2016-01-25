#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.fetch.article.weixin import fetch_article_list


def test_fetch_article_list():
    gk_user = {'pk': 1,
    'weixin_id': u'shenyebagua818',
    'weixin_openid': None,
    'weixin_qrcode_img': u'images/89ff3b39797b0f2a429319f2fca00081.jpg'}
    openid = 'oIWsFtyGRm3FRZuQbcDquZOI5N_E'
    ext = 'zBO3BL4RDTQCk5VnTFARJ9CxHUokEvDjyG97ZTG9sp4asGGQ_mNo6oMnlSzSPZO6'
    resp = fetch_article_list(gk_user, openid, ext)



