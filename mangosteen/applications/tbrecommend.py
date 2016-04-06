# -*- coding: utf-8 -*-

from flask import Flask
import top.api
import top
import json
# import time

from model.taobao_token import TaobaoToken

app = Flask(__name__)
app.config.from_pyfile('../config/default.py')


def handel(keyword, **kwargs):
    app_key = app.config.get('APP_KEY')
    app_secret = app.config.get('APP_SECRET')

    req = top.api.AlibabaOrpRecommendRequest()
    req.set_app_info(top.appinfo(app_key, app_secret))
    req.appid=2750
    req.call_source="TOP_GUOKU"

    istk = kwargs.pop('istk', True)
    ismall = kwargs.pop('ismall', False)
    count = kwargs.pop('count', 20)
    user_id = kwargs.pop('user_id', None)
    params = dict()

    if user_id:
        taobao = TaobaoToken.query.filter_by(user_id=user_id).first()
        print "taobao %s screen_name %s" %  (taobao.open_uid, taobao.screen_name)
        params.update({
            'userid': taobao.taobao_id,
            # 'userid': taobao.isv_uid
        })


    params.update(
        {
            "istk":     str(istk),
            "mall":     str(ismall),
            "count":    count,
        }
    )

    if keyword:
        params.update({
            'keyword':keyword,
        })
    app.logger.info(params)
    req.params = json.dumps( params )

    try:
        # access_time = time.time()
        resp= req.getResponse(timeout=5)
        res = resp['alibaba_orp_recommend_response']['recommend']
        return res
    except Exception, e:
        app.logger.error(e)
        return None

