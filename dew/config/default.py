DEBUG       = False

SQLALCHEMY_DATABASE_URI         = "mysql://dolphin:dolphin123@10.0.2.125:13306/dolphin?charset=utf8mb4"
SQLALCHEMY_BINDS                = {
                                    'article' :'mysql://guoku:guoku!@#@10.0.2.95/core',
                                }
SQLALCHEMY_TRACK_MODIFICATIONS  = True
SQLALCHEMY_POOL_RECYCLE         = 3600

