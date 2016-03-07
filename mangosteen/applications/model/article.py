from base import db
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT


class Article(db.Model):
    __tablename__       = "core_article"

    id                  = db.Column(db.INTEGER(11), primary_key=True)
    creator_id          = db.Column(db.INTEGER(11))
    title               = db.Column(db.VARCHAR(255))
    content             = db.Column(db.Text())
    created_datetime    = db.Column(db.DateTime())
    updated_datetime    = db.Column(db.DateTime())
    cover               = db.Column(db.VARCHAR(255))


