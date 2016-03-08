from base import db
# from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT


class Article(db.Model):
    __tablename__       = "core_article"
    # (remove, draft, published) = xrange(3)
    # ARTICLE_STATUS_CHOICES = [
    #     (published, _("published")),
    #     (draft, _("draft")),
    #     (remove, _("remove")),
    # ]
    ARTICLE_STATUS_CHOICES = ("remove", "draft","published")

    id                  = db.Column(db.Integer(), primary_key=True)
    creator_id          = db.Column(db.Integer())
    title               = db.Column(db.VARCHAR(255))
    cleaned_title       = db.Column(db.VARCHAR(255))
    cover               = db.Column(db.VARCHAR(255))
    # publish             = db.Column(db.Enum, ARTICLE_STATUS_CHOICES)
    content             = db.Column(db.Text())
    created_datetime    = db.Column(db.DateTime())
    updated_datetime    = db.Column(db.DateTime())
    showcover           = db.Column(db.Boolean(), default=False)
    read_count          = db.Column(db.Integer(), default=0)
    feed_read_count     = db.Column(db.Integer(), default=0)


