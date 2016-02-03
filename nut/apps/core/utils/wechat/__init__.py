import  requests
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
    res = requests.get(url)
    token = res.json().access_token
    expires = res.json().expires_in

    cache.set(key, token , expires-100)

    return token


def get_jsapi_ticket():
    key = get_jsapi_ticket_key()
    ticket = cache.get(key, None)
    if not ticket is None:
        return ticket

    token = get_wechat_access_token()
    res = requests.get(get_jsapi_ticket_request_url(token))
    ticket = res.json().ticket
    errcode = res.json().errcode
    expires = res.json().expires_in
    if errcode == 0:
        cache.set(key, ticket, expires-100)
        return ticket
    else:
        raise Exception('get wechat jsapi ticket error')







