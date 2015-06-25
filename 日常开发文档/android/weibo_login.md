http://api.guoku.com/mobile/v4/weibo/login/

POST : {
    sina_id:  微博授权来的 
    sina_token:  微博授权来的
    screen_name:  微博授权来的
    api_key:  果库的 API_KEY
}

Return :
{
    'user':  用户对象的 JSON
    'session' : session_key
}