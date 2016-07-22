# -*- coding: utf-8 -*-

from flask_restful import reqparse, abort, Resource

from applications.models.searchhistory import SearchHistory
from applications.schema.searchhistory import SearchHistorySchema

search_history_schema = SearchHistorySchema()
search_history_schema_list = SearchHistorySchema(many=True)
#
get_parser = reqparse.RequestParser()
get_parser.add_argument(
    'p', dest='page',
    location='args', type = int,
    default = 1,
)
get_parser.add_argument(
    'size', dest='size',
    location='args', type = int,
    default = 30,
)


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
        args =  get_parser.parse_args()
        paginator = SearchHistory.query.paginate(args['page'], args['size'], False)
        # return search_history_schema_list.dump(paginator.items).data, 200
        res = {
            'page': args['page'],
            'size': args['size'],
            'data': search_history_schema_list.dump(paginator.items),
            'total': paginator.total,
        }
        return res, 200

    def post(self):
        args = post_parser.parse_args()
        sh = SearchHistory(user_id=args['user_id'], keyword=args['keyword'],
                           ip=args['ip'], user_agent=args['user_agent'])
        sh.save()
        # sh.close()
        return search_history_schema.dump(sh).data, 201


class UserSearchHistoryView(Resource):

    def get(self, user_id):
        assert user_id is not None
        args = get_parser.parse_args()
        paginator = SearchHistory.query.filter_by(user_id=user_id).\
                                    paginate(args['page'], args['size'], False)

        res = {
            'page': args['page'],
            'data': search_history_schema_list.dump(paginator.items),
            'total': paginator.total,
        }
        return res, 200
        # return search_history_schema_list.dump(paginator.items).data, 200