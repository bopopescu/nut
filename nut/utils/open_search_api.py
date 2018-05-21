# coding=utf-8
import base64
import hashlib
import hmac
import json
import random
import time
import urllib
from hashlib import sha1
from pprint import pprint

import requests


class V3Api(object):
    VERB = 'POST'

    def __init__(self, endpoint='', access_key='', secret='', app_name=''):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret = secret
        self.app_name = app_name

    def search(self, table_name, params):
        """
        搜索
        :param table_name: str
        :type params: object
        """
        uri = '/v3/openapi/apps/{}/search'.format(self.app_name)
        query, header = self.build_query(uri=uri, method='GET', body='', http_params=params)
        # print('query:', query)
        # print('header:', header)
        url = self.endpoint + query
        resp = requests.get(url,  headers=header, params=params)
        return resp.json()

    def bulk_update(self, table_name, data):
        """
        批量上传数据
        :param table_name: str
        :param data: list
        :return:
        """
        body_json = json.dumps(data) if isinstance(data, list) else data
        body_json = body_json.encode('utf-8')
        uri = '/v3/openapi/apps/{}/{}/actions/bulk'.format(self.app_name, table_name)
        query, header = self.build_query(uri=uri, method='POST', body=json.dumps(data))
        url = self.endpoint + query
        resp = requests.post(url, data=body_json, headers=header)
        return resp.json()

    def build_query(self,
                    uri,
                    method,
                    body,
                    http_header=None,
                    http_params=None):
        if http_params is None:
            http_params = {}
        if http_header is None:
            http_header = {}

        request_header = self.build_request_header(uri=uri,
                                                   method=method,
                                                   body=body,
                                                   http_params=http_params,
                                                   http_header=http_header)

        return uri, request_header

    def build_authorization(self, uri, method, http_params, request_header):
        canonicalized = u'\n'.join([
            method.upper(),
            request_header['Content-MD5'],
            request_header['Content-Type'],
            request_header['Date'],
            V3Api.__canonicalized_headers(request_header),
            V3Api.__canonicalized_resource(uri, http_params)
        ])


        h = hmac.new(self.secret, canonicalized, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return 'OPENSEARCH {}:{}'.format(self.access_key, signature)

    @staticmethod
    def __canonicalized_headers(request_header):
        header = {key.strip(' \t'): value.strip(' \t') for key, value in request_header.iteritems()
                  if key.startswith('X-Opensearch-') and value}

        canonicalized = u'\n'.join((u'{}:{}'.format(key.lower(), header[key]) for key in sorted(header.iterkeys())))
        return canonicalized

    @staticmethod
    def __canonicalized_resource(uri, http_params):
        canonicalized = urllib.quote(uri).replace(u'%2F', u'/')
        params = [u'{}={}'.format(urllib.quote(key), urllib.quote(http_params[key].encode('utf-8')))
                  for key in sorted(http_params.iterkeys()) if http_params[key]]

        if params:
            canonicalized += u'?' + u'&'.join(params)
        return canonicalized

    def __canonicalizedResource(self, uri, http_params):
        canonicalized = urllib.quote(uri).replace('%2F', '/')

        sorted_params = sorted(http_params.items(), key=lambda http_params: http_params[0])
        params = []
        for (key, value) in sorted_params:
            if value is None or len(value) == 0:
                continue

            params.append(urllib.quote(key) + '=' + urllib.quote(value))

        return canonicalized + '?' + '&'.join(params)

    @staticmethod
    def generate_date():
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @staticmethod
    def generate_nonce():
        return str(int(time.time() * 100)) + str(random.randint(1000, 9999))

    def build_request_header(self, uri, method, body, http_params, http_header):
        request_header = {key: value for key, value in http_header.iteritems() if value is not None}
        request_header.update({
            'Content-MD5': hashlib.md5(body.encode('utf-8')).hexdigest() if body else '',
            'Content-Type': 'application/json',
            'Date': V3Api.generate_date(),
            'X-Opensearch-Nonce': V3Api.generate_nonce(),
        })
        request_header['Authorization'] = self.build_authorization(uri, method, http_params, request_header)

        return request_header


if __name__ == '__main__':
    access_key_id = 'LTAIfykGdJqG9Q2D'
    access_key_secret = 'Ylbpdw415TNmGYbGSIPyGV8UcQxr1V'
    HOST = 'http://opensearch-cn-beijing.aliyuncs.com'
    APP_NAME = 'guoku_search'

    api = V3Api(endpoint=HOST, access_key=access_key_id, secret=access_key_secret, app_name=APP_NAME)

    # payload = [
    #     {
    #         'cmd': 'add',
    #         'fields': {
    #             'id': 10,
    #             'title': u'测试项目，最新Android',
    #             'intro': u'这里是介绍',
    #             'brand': u'Google'
    #         }
    #     }
    # ]
    # pprint(api.bulk_update('entity', payload))

    params = {
        'query': u"query=default:'apple'",
        # 'query': u"query=name:'搜索'&&config=start:0,hit:1,format:json&&sort=+id",
        # 'fetch_fields': 'id;name'
    }

    data = api.search('entity', params)
    ids = [d['id'] for d in data['result']['items']]
    pprint(ids)
    # pprint(data['result']['items'])
    # pprint(api.search('entity', params))
