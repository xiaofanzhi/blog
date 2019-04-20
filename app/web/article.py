from . import web
from flask import current_app
from flask import render_template,request,url_for,redirect,flash
from app.models.auth import User
from app.models.article import Article
from app.ext import db
# 登录用
from flask_login import login_user, login_required


@web.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = Article.query.order_by(
        Article.created.desc()).paginate(page,per_page=current_app.config['PER_PAGE'],
                                         error_out=False)

    articles = pagination.items
    return  render_template('index.html',articles=articles,pagination=pagination, endpoint='.index')
