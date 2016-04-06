from base import db

class TaobaoToken(db.Model):

    __tablename__   = 'core_taobao_token'

    id              = db.Column(db.Integer(), primary_key=True)
    user_id         = db.Column(db.Integer())
    taobao_id       = db.Column(db.Integer())
    screen_name     = db.Column(db.VARCHAR(64))
    open_uid        = db.Column(db.VARCHAR(64))
    isv_uid         = db.Column(db.VARCHAR(64))

    def __repr__(self):
        return "<Taobao User Name %r>" % self.screen_name