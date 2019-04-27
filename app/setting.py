import os

# 公用配置信息
class Config:
    SQLALCHEMY_DATABASE_URI_DEV = 'mysql+cymysql://root:root@localhost:3306/blog'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEYS = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*2'
    SECRET_KEY = os.environ.get('SECRET_KEY') or SECRET_KEYS

    PER_PAGE = 10
    COMMENT_PER_PAGE = 30
    SAVEPIC = 'app/static/upload/'



# 生产
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI_DEV


# 开发
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI_DEV



config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}



