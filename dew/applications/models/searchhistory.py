# -*- coding: utf-8 -*-

from base import db
from base import BaseModel, TimestampMixin
# from sqlalchemy_utils import IPAddressType


class SearchHistory(BaseModel, TimestampMixin):

    __tablename__               =   'search_history'

    id                          =   db.Column(db.Integer(), primary_key=True)
    user_id                     =   db.Column(db.Integer(), index=True)
    result_count                =   db.Column(db.Integer(), default=0)
    keyword                     =   db.Column(db.VARCHAR(255))
    ip                          =   db.Column(db.CHAR(45))
    user_agent                  =   db.Column(db.VARCHAR(255))

    # def __repr__(self):
    #     return "<Keyword: {0} from IP {1}>".format(self.keyword, self.ip)


    def __init__(self, *args, **kwargs):
        self.user_id        = kwargs.pop('user_id', None)
        # assert self.user_id is not None
        self.keyword        = kwargs.pop('keyword', None)
        self.ip             = kwargs.pop('ip', None)
        self.user_agent     = kwargs.pop('user_agent', None)
        self.result_count   = kwargs.pop('result_count', 0)
