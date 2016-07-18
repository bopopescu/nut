from base import db
from base import BaseModel, TimestampMixin


class SearchHistory(TimestampMixin, BaseModel):

    __tablename__               =   'search_history'

    id                          =   db.Column(db.Interger(), primary_key=True)
    user_id                     =   db.Column(db.Interger())
    keyword                     =   db.Column(db.VARCHAR(255))
