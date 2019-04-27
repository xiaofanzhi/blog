from flask import Flask
from .ext import db, login_manager, moment, bootstrap
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_babelex import Babel
from .view_model.processor import utility_processor
from app.models import *
from flask_bootstrap import Bootstrap

from .setting import config


def creat_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap = Bootstrap(app)
    db.init_app(app)
    db.create_all(app=app)

    register_blueprint(app)
    moment.init_app(app)


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


    # admin 注册
    from .admin import admin
    admin.init_app(app)
    # 汉化
    babel = Babel(app)
    babel.init_app(app)
    '''
    app_context_processor在flask中被称作上下文处理器，借助app_context_processor
    可以让所有自定义变量在模板中可见
    函数的返回结果必须是dict，dict中的key将作为变量在所有模板中可见
    '''
    app.context_processor(utility_processor)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)






