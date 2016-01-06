#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from time import sleep

import pytest

from apps.fetch import WeChatArticle


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')


def test_cache_data(we_chat_id_list):
    for account_id in we_chat_id_list:
        we_chat_fetcher = WeChatArticle(account_id)
        file_path = '%s/%s_%s.html' % (data_dir, 'wechat_search', account_id)
        if not os.path.isfile(file_path):
            html_file = codecs.open(file_path, 'w', 'utf-16')
            we_chat_fetcher.get_search_page()
            source = we_chat_fetcher.search_page
            html_file.write(source)
            html_file.close()
            sleep(5)



@pytest.mark.parametrize('account_id,account_url', (
    ('shenyebagua818', 'http://weixin.sogou.com/gzh?openid=oIWsFtyGRm3FRZuQbcDquZOI5N_E&ext=meTK-Q6CgYT-DHYcIW5N0QuLU0A0H8QrFacyt8v_4EFWeLmCEODO-76hqX7M_eqC'),
    ('a529597', 'http://weixin.sogou.com/gzh?openid=oIWsFt9wW05QWFFlh954q_SV0sno&ext=meTK-Q6CgYTnmA-kFXWE58-NoW1u7Az0c_t_0ikjl3T-19yoGNYbJlB8Nz39oXd3'),
    ('bb2b2bb', 'http://weixin.sogou.com/gzh?openid=oIWsFt1sT7UB3WgapFp74dPEOHLI&ext=meTK-Q6CgYTzZWuCBqVglE9aohPlWezOYL4Z84eWtkwsazuwG4XLUg6XHmeCX9tX'),
    ('cctvnewscenter', 'http://weixin.sogou.com/gzh?openid=oIWsFt_IC706OXjJP2sn_T5MxVfs&ext=meTK-Q6CgYQMurv9tdWeCmKXvijwLV51TYLhH5_MLMu8-_qivMTUYMJffEFCEzgG'),
    ('woshitongdao', 'http://weixin.sogou.com/gzh?openid=oIWsFt6Jz41fAg2eQHTA1wIbSp0Y&ext=meTK-Q6CgYQiHRHfpAoUgrf3ZB6pO_uo82mkdfw6Ht40TYbBSvx1o8e1XtFGhyXB'),
))
def test_fetch_account(account_id, account_list_url):
    we_chat_fetcher = WeChatArticle(account_id)
    source_file = open('%s/%s_%s.html' % (data_dir, 'wechat_search', account_id), 'r')
    html_source = source_file.read()
    we_chat_fetcher.search_page = html_source
    source_file.close()
    assert we_chat_fetcher.account_list_url == account_list_url
