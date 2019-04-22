from . import web
from flask import current_app, abort
from flask import render_template,request,url_for,redirect,flash
from app.models.auth import User
from app.models.article import Article, Tag
from app.ext import db
# 登录用
from flask_login import login_user, login_required



@web.route('/tag/<name>/')
def tag(name):
    page = int(request.args.get('page', 1))
    tag = Tag.query.filter_by(name=name).first_or_404()
    _query = Article.query.filter(Article.tags.any(id=tag.id)).order_by(
        Article.created.desc())
    pagination = _query.paginate(page,per_page=current_app.config['PER_PAGE'],
                                          error_out=False)
    articles = pagination.items
    return render_template('index.html',articles=articles,tag=tag,
                           pagination=pagination,endpoint='.index',select_tag=tag)

