# -*- coding: utf-8 -*-
from flask import Flask
from flask import Response, request, abort
from flask_json import FlaskJSON, json_response
from tbrecommend import handel
import jieba.analyse
from model import *

jieba.load_userdict("user_dict.txt")
# jieba.set_dictionary("dict.txt.small")
# jieba.set_dictionary("user_dict.txt")
jieba.analyse.set_idf_path("idf.txt.big")
jieba.analyse.set_stop_words("stop_words.txt")

app = Flask(__name__)


app.config.from_pyfile('../config/default.py')
FlaskJSON(app)



@app.route('/recommend', methods=['GET'])
def recommend():
    assert request.path == '/recommend'
    assert request.method == "GET"

    keyword = request.args.get('keyword', None)
    # itemId = request.args.get('itemid', None)
    user_id = request.args.get('uid', None)
    istk = request.args.get('tk', True)
    ismall = request.args.get('mall', False)
    count = request.args.get('count', 20)

    res = handel(keyword=keyword, istk=istk, ismall=ismall, count=count, user_id=user_id)
    if res is None:
        abort(404)
    return Response(res, mimetype="application/json")
    # return jsonify(res['alibaba_orp_recommend_response']['recommend'])


@app.route('/textrank', methods=['POST'])
def textrank():
    text = request.form.get('text', None)
    res = jieba.analyse.textrank(text.encode('utf-8'), topK=20, withWeight=True, allowPOS=('ns', 'n'))
    return json_response(res = res)


from textrank import get_textrank
@app.route('/article/<int:article_id>', methods=['GET'])
def article_textrank(article_id):
    title, content = get_textrank(article_id)
    if title is None:
        abort(404)
    return json_response(title=title, content = content)
    # return "ok"


if __name__ == '__main__':
    # print app.config.get('APP_KEY')
    app.debug = True
    app.run(host="0.0.0.0")
