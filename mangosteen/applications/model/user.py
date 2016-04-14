from base import db


class User(db.Model):
    __tablename__   = "core_gkuser"

    id              = db.Column(db.Integer(), primary_key=True)
    password        = db.Column(db.VARCHAR(128))
    last_login      = db.Column(db.DateTime())
    is_superuser    = db.Column(db.Boolean())
    email           = db.Column(db.VARCHAR(255))

    def __repr__(self):
        return "<User e-Mail %r>" % self.email
