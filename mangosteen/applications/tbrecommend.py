# -*- coding: utf-8 -*-

from flask import Flask
import top.api
import top
import json
from werkzeug.contrib.cache import FileSystemCache

from model.taobao_token import TaobaoToken


app = Flask(__name__)
app.config.from_pyfile('../config/default.py')

# cache = SimpleCache()
cache = FileSystemCache(cache_dir='/tmp/cache/')

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
        # print "taobao %s screen_name %s" %  (taobao.open_uid, taobao.screen_name)
        if taobao:
            params.update({
                'userid': taobao.taobao_id,
            # 'userid': taobao.isv_uid
            })

        item_key = "item:{0}-user:{1}".format(keyword.encode('utf-8'), user_id)
    else:
        item_key = "item:{0}".format(keyword.encode('utf-8'))

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
    # app.logger.info(params)
    req.params = json.dumps( params )

    res = cache.get(item_key)
    # print res
    if res is None:
        try:
            # access_time = time.time()
            resp= req.getResponse(timeout=5)
            res = resp['alibaba_orp_recommend_response']['recommend']
            cache.set(item_key, res, timeout=86400)
            # return res
        except Exception, e:
            app.logger.error(e)
            return None
    # else:
    return res
