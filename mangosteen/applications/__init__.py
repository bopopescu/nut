from flask import Flask
from flask import Response, request, abort
from flask_json import FlaskJSON, json_response
from tbrecommend import handel
import jieba.analyse

jieba.analyse.set_stop_words("stop_words.txt")
jieba.analyse.set_idf_path("idf.txt.big")


app = Flask(__name__)
app.config.from_pyfile('../config/default.py')
FlaskJSON(app)


@app.route('/recommend', methods=['GET'])
def recommend():
    assert request.path == '/recommend'
    assert request.method == "GET"

    keyword = request.args.get('keyword', None)
    # itemId = request.args.get('itemid', None)
    istk = request.args.get('tk', True)
    ismall = request.args.get('mall', False)
    count = request.args.get('count', 20)

    res = handel(keyword=keyword, istk=istk, ismall=ismall, count=count)
    # print res
    if res is None:
        abort(404)
    return Response(res, mimetype="application/json")
    # return jsonify(res['alibaba_orp_recommend_response']['recommend'])


@app.route('/textrank', methods=['POST'])
def textrank():
    text = request.form.get('text', None)
    res = jieba.analyse.textrank(text.encode('utf-8'), topK=20, withWeight=True, allowPOS=('ns', 'n'))
    return json_response(res = res)


if __name__ == '__main__':
    # print app.config.get('APP_KEY')
    app.debug = True
    app.run(host="0.0.0.0")
