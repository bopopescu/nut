import  requests
from datetime import datetime
import random
import hashlib
from django.core.cache import cache



APPID = 'wx7b445b01ad2bfe9e'
APPSECRET = '37b28c446bd2187d99588ce85fc8b5a6'


def get_token_request_url(appid=APPID, appsec=APPSECRET):
    return 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsec)

def get_access_token_cache_key():
    return 'wechat:access_token:for:%s' % APPID

def get_jsapi_ticket_request_url(token):
    return 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token

def get_jsapi_ticket_key():
    return 'wechat:jsapi_ticket:for:%s' % APPID

def get_wechat_access_token():
    key  = get_access_token_cache_key()

    token = cache.get(key, None)
    if not token is None:
        return token

    url = get_token_request_url()
    res = requests.get(url,verify=False)
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
    sigSha1 = hashlib.sha1()
    sigSha1.update(queryString)
    sig_obj['signature'] = sigSha1.hexdigest()
    return sig_obj

















