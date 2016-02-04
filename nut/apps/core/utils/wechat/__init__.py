# coding=utf-8

import  requests
from datetime import datetime
import random
import hashlib
from django.core.cache import cache

# 开发者ID
# AppID(应用ID)wx728e94cbff8094df
# AppSecret(应用密钥)d841a90cf90d00f145ca22b82e12a500 隐藏 重置


APPID = 'wx728e94cbff8094df'
APPSECRET = 'd841a90cf90d00f145ca22b82e12a500'


def get_token_request_url(appid=APPID, appsec=APPSECRET):
    return 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsec)

def get_access_token_cache_key():
    return 'wechat:access_token:for:%s' % APPID

def get_jsapi_ticket_request_url(token):
    return 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token

def get_jsapi_ticket_key():
    return 'wechat:jsapi_ticket:for:%s' % APPID

def clear_cached_wechat_values():
    token_key = get_access_token_cache_key()
    jsapi_ticket_key = get_jsapi_ticket_key()
    cache.set(token_key, None)
    cache.set(jsapi_ticket_key, None)



def get_wechat_access_token():
    key  = get_access_token_cache_key()

    token = cache.get(key, None)
    if not token is None:
        return token

    url = get_token_request_url()
    res = requests.get(url,verify=False)

    if hasattr(res.json(), 'errcode')  and res.json()['errcode'] != 0:
        clear_cached_wechat_values()
        raise Exception('token need refresh')
        return None

    token = res.json()['access_token']
    expires = res.json()['expires_in']

    cache.set(key, token , expires-100)

    return token


def get_jsapi_ticket():
    key = get_jsapi_ticket_key()
    ticket = cache.get(key, None)
    if not ticket is None:
        return ticket

    token = get_wechat_access_token()
    res = requests.get(get_jsapi_ticket_request_url(token),verify=False)

    if  hasattr(res.json(), 'errcode')  and  res.json()['errcode'] != 0:
        clear_cached_wechat_values()
        raise Exception('jsapi need refresh')
        return None

    ticket = res.json()['ticket']
    errcode = res.json()['errcode']
    expires = res.json()['expires_in']
    if errcode == 0:
        cache.set(key, ticket, expires-100)
        return ticket
    else:
        raise Exception('get wechat jsapi ticket error')


def get_nonce_str():
    charList = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    strLen = 16
    randStr = ''
    for i in xrange(strLen):
        randStr += charList[random.randrange(len(charList))]
    return randStr


def get_js_sdk_signature_obj(sig_url=None,):
    if sig_url is None:
        raise Exception('need sig_url param , for url of the page need to be signed')

    sig_obj = {
                'noncestr': get_nonce_str()
               ,'jsapi_ticket':get_jsapi_ticket()
               ,'timestamp':datetime.now().strftime('%s')
               ,'url':sig_url
               }
    queryString  = ''
    keys = sig_obj.keys()
    keys.sort()
    for key in keys:
        queryString += (key + '=' + sig_obj[key] + '&')
    queryString = queryString[0:-1]
    sig = hashlib.sha1(queryString.encode('utf-8')).hexdigest()
    sig_obj['signature'] = sig
    sig_obj['appid'] = APPID
    return sig_obj