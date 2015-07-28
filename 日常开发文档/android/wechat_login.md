http://api.guoku.com/mobile/v4/wechat/login/

POST : {
    unionid:   ID 
    nickname:  微信NICK
    headimgurl:  头像URL
    api_key:  果库的 API_KEY
}

Return :
{
    'user':  用户对象的 JSON
    'session' : session_key
}