http://api.guoku.com/mobile/v4/baichuan/login/

POST : {
    user_id:  淘宝授权来的 user_id （ 也就是 淘宝 token ）
    nick:     淘宝授权来的 NICK NAME
    api_key:  果库的 请求的 API_KEY
}

Return :
{
    'user':  用户对象的 JSON
    'session' : session_key
}