from app.models.article import Category
from . import web
from flask import current_app, abort
from flask import render_template,request,url_for,redirect,flash
from app.models.auth import User
from app.models.article import Article
from app.ext import db


@web.route('/category/<int:id>/')
def category(id):
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.get_or_404(id).articles.order_by(
        Article.created.desc()).paginate(page,per_page=current_app.config['PER_PAGE'],
                                         error_out=False)
    articles = pagination.items
    return render_template('index.html',articles=articles,
                           pagination=pagination, endpoint='.category',
                           id=id, category_id=id)