from flask import Flask
from flask import Response, request, jsonify

from tbrecommend import handel
# from top import api

app = Flask(__name__)
app.config.from_pyfile('../config/default.py')


@app.route('/recommend', methods=['GET'])
def recommend():
    assert request.path == '/recommend'
    assert request.method == "GET"

    keyword = request.args.get('keyword')
    res = handel(keyword)
    # print res
    return Response(res, mimetype="application/json")
    # return jsonify(res['alibaba_orp_recommend_response']['recommend'])

if __name__ == '__main__':
    # print app.config.get('APP_KEY')
    app.run()
