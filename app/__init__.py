from flask import Flask
from .ext import db, login_manager, moment, bootstrap
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand



def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    db.init_app(app)
    db.create_all(app=app)

    register_blueprint(app)



    # 让python支持命令行工作
    manager = Manager(app)

    # 使用migrate绑定app和db
    migrate = Migrate(app, db)
    # 添加迁移脚本的命令到manager中
    manager.add_command('db', MigrateCommand)

    # login 登录插件初始化
    login_manager.init_app(app)
    # 没登录，将其引导到登录页面
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录'


    # # admin 注册
    # from .admin import admin
    # admin.init_app(app)
    # # 汉化
    # babel = Babel(app)
    # babel.init_app(app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)



