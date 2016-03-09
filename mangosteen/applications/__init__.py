from flask import Flask
from flask import Response, request, abort
from flask_json import FlaskJSON, json_response
from tbrecommend import handel
import jieba.analyse
from model.base import db
from model import *
import click
from flask_cli import FlaskCLI

jieba.analyse.set_stop_words("stop_words.txt")
jieba.analyse.set_idf_path("idf.txt.big")

app = Flask(__name__)


app.config.from_pyfile('../config/default.py')
FlaskJSON(app)
FlaskCLI(app)


def init_db():
    db.create_all()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


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


from textrank import get_textrank
@app.route('/article/<int:article_id>', methods=['GET'])
def article_textrank(article_id):
    res = get_textrank(article_id)
    return json_response(content = res)
    # return "ok"


if __name__ == '__main__':
    # print app.config.get('APP_KEY')
    app.debug = True
    app.run(host="0.0.0.0")
