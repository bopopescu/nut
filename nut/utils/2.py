# -- coding: utf-8 --
import md5, time, random, hmac, base64, copy
import urllib
from hashlib import sha1
import httplib
import collections
from pprint import pprint

import requests


class V3Api:
    # 定义变量
    URI_PREFIX = '/v3/openapi/apps/'
    OS_PREFIX = 'OPENSEARCH'

    def __init__(self, address='', port=''):
        self.address = address
        self.port = port

    def runQuery(self,
                 app_name=None,
                 access_key=None,
                 secret=None,
                 http_header={},
                 http_params={}):
        query, header = self.buildQuery(app_name=app_name,
                                        access_key=access_key,
                                        secret=secret,
                                        http_header=http_header,
                                        http_params=http_params)

        url = self.address + query
        print(url)
        resp = requests.get(url, headers=header)
        return resp.json()
        # conn = httplib.HTTPConnection(self.address, self.port)

        # conn.request("GET", url=query, headers=header)
        # response = conn.getresponse()

        # return response.status, response.getheaders(), response.read()

    def buildQuery(self,
                   app_name=None,
                   access_key=None,
                   secret=None,
                   http_header={},
                   http_params={}):
        uri = self.URI_PREFIX
        if app_name is not None:
            uri += app_name
        uri += '/search'

        param = []
        for key, value in http_params.iteritems():
            param.append(urllib.quote(key) + '=' + urllib.quote(value))

        query = ('&'.join(param))

        request_header = self.buildRequestHeader(uri=uri,
                                                 access_key=access_key,
                                                 secret=secret,
                                                 http_params=http_params,
                                                 http_header=http_header)

        return uri + '?' + query, request_header

    # 签名实现
    def buildAuthorization(self, uri, access_key, secret, http_params, request_header):
        canonicalized = 'GET\n' \
                        + self.__getHeader(request_header, 'Content-MD5', '') + '\n' \
                        + self.__getHeader(request_header, 'Content-Type', '') + '\n' \
                        + self.__getHeader(request_header, 'Date', '') + '\n' \
                        + self.__canonicalizedHeaders(request_header) \
                        + self.__canonicalizedResource(uri, http_params)

        print('canonicalized: ', canonicalized)
        h = hmac.new(secret, canonicalized, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return '%s %s%s%s' % (self.OS_PREFIX, access_key, ':', signature)

    def __getHeader(self, header, key, default_value=None):
        if key in header and header[key] is not None:
            return header[key]
        return default_value

    def __canonicalizedResource(self, uri, http_params):
        canonicalized = urllib.quote(uri).replace('%2F', '/')

        sorted_params = sorted(http_params.items(), key=lambda http_params: http_params[0])
        params = []
        for (key, value) in sorted_params:
            if value is None or len(value) == 0:
                continue

            params.append(urllib.quote(key) + '=' + urllib.quote(value))

        return canonicalized + '?' + '&'.join(params)

    def generateDate(self, format="%Y-%m-%dT%H:%M:%SZ", timestamp=None):
        if timestamp is None:
            return time.strftime(format, time.gmtime())
        else:
            return time.strftime(format, timestamp)

    def generateNonce(self):
        return str(int(time.time() * 100)) + str(random.randint(1000, 9999))

    def __canonicalizedHeaders(self, request_header):
        header = {}
        for key, value in request_header.iteritems():
            if key is None or value is None:
                continue
            k = key.strip(' \t')
            v = value.strip(' \t')
            if k.startswith('X-Opensearch-') and len(v) > 0:
                header[k] = v

        if len(header) == 0:
            return ''

        sorted_header = sorted(header.items(), key=lambda header: header[0])
        canonicalized = ''
        for (key, value) in sorted_header:
            canonicalized += (key.lower() + ':' + value + '\n')

        return canonicalized

    # 构建请求 Header 参数
    def buildRequestHeader(self, uri, access_key, secret, http_params, http_header):
        request_header = copy.deepcopy(http_header)
        if 'Content-Type' not in request_header:
            request_header['Content-Type'] = 'application/json'
        if 'Date' not in request_header:
            request_header['Date'] = self.generateDate()
        if 'X-Opensearch-Nonce' not in request_header:
            request_header['X-Opensearch-Nonce'] = self.generateNonce()
        if 'Authorization' not in request_header:
            request_header['Authorization'] = self.buildAuthorization(uri,
                                                                      access_key,
                                                                      secret,
                                                                      http_params,
                                                                      request_header)
        key_del = []
        for key, value in request_header.iteritems():
            if value is None:
                key_del.append(key)

        for key in key_del:
            del request_header[key]

        return request_header


if __name__ == '__main__':
    accesskey_id = 'LTAIfykGdJqG9Q2D'
    accesskey_secret = 'Ylbpdw415TNmGYbGSIPyGV8UcQxr1V'
    # 下面的值替换为应用访问api地址，例如  opensearch-cn-hangzhou.console.aliyun.com
    internet_host = 'http://opensearch-cn-beijing.aliyuncs.com'
    appname = 'guoku_search'

    api = V3Api(address=internet_host, port='80')
    # 下面为设置查询信息，query参数中可设置对应的查询子句，添加查询参数，参考fetch_fields用法
    query_subsentences_params = {
        'query': u"query=default:'apple'",
        # 'query': "query=default:'apple'&&config=start:0,hit:1,format:json&&sort=+id",
        # 'fetch_fields': 'id;name'
    }
    pprint(api.runQuery(app_name=appname, access_key=accesskey_id, secret=accesskey_secret,
                        http_params=query_subsentences_params, http_header={}))
