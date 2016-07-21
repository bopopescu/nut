# -*- coding: utf-8 -*-

from flask_restful import reqparse, abort, Resource

from applications.models.searchhistory import SearchHistory
from applications.schema.searchhistory import SearchHistorySchema

search_history_schema = SearchHistorySchema()
search_history_schema_list = SearchHistorySchema(many=True)
#
# get_parser  = reqparse.RequestParser()
# get_parser.add_argument(
#     # 's', dest='site',
#     # required=True,
# )


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'uid', dest='user_id',
    location='form', type=int,
    help='The user\'s user id',
)

post_parser.add_argument(
    'key', dest='keyword',
    location='form', required=True,
    help='keyword form user search action',
)

post_parser.add_argument(
    'ip', dest='ip',
    location='form', required=True,
    help='remote ip'
)

post_parser.add_argument(
    'ua', dest='user_agent',
    location='form', required=True,
    help='user agent'
)


class SearchHistoryView(Resource):

    def get(self):
        sh = SearchHistory.query.all()
        # print sh
        return search_history_schema_list.dump(sh).data, 200

    def post(self):

        args = post_parser.parse_args()
        sh = SearchHistory(user_id=args['user_id'], keyword=args['keyword'],
                           ip=args['ip'], user_agent=args['user_agent'])
        sh.save()
        return search_history_schema.dump(sh).data, 201



