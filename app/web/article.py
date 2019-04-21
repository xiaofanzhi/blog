from . import web
from flask import current_app, abort
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



# 文章详细
@web.route('/article/<int:id>/', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get_or_404(id)
    if not article.published:
        abort(404)
    next = next_article(article)
    prev = prev_article(article)

#     单纯展示 还没有关联评论

     # page = request.args.get('page',1,type=int)
    return  render_template('article.html',article=article,next_article=next,prev_article=prev,)

# 下一篇文章 列表中降序排序
def next_article(article):
    article_list = Article.query.order_by(Article.created.desc()).all()
    articles = [article for article in article_list if article.published]
    if articles[0] != article:
        next_post = articles[articles.index(article)-1]
        return next_post
    return None


def prev_article(article):
    article_list = Article.query.order_by(Article.created.desc()).all()
    articles = [article for article in article_list if article.published]
    if articles[-1] != article:
        next_post = articles[articles.index(article)+1]
        return next_post
    return None
