class Config:
    DEBUG = False
    TESTING = False
    # mysql+pymysql://user:password@host:port/database
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://gjp:976431@49.235.194.73:3306/test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'hdfjds38948938bmbfsd90008'


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DATABASE_URI = ''


class TestingConfig(Config):
    TESTING = True
