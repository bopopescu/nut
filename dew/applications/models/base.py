from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('../../config/default.py')
db = SQLAlchemy(app)
ma = Marshmallow()



class BaseModel(db.Model):
    __abstract__        = True
    __table_args__      = {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}
    # _column_name_sets = NotImplemented

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def close(self):
        db.session.remove()

    # def to_dict(self):
    #     return {c.name: "%s" % getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.now(), index=True)
