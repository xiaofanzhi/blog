from . import web
from flask import current_app, abort
from flask import render_template,request,url_for,redirect,flash
from app.models.auth import User
from app.models.article import Article
from app.ext import db
# 登录用
from flask_login import login_user, login_required



@web.route('/archives')
def archives():
    count = Article.query.count()
    page = request.args.get('page',1,type=int)
    pagination = Article.query.order_by(Article.created.desc()).paginate(
                page, per_page=current_app.config['PER_PAGE'],
                error_out=False
    )
    articles = [article for article in pagination.items if article.published]
    year = list(set([i.year for i in articles]))[::-1]
    data = {}
    year_article = []
    for y in year:
        for p in articles:
            if y==p.year:
                year_article.append(p)
                data[y] = year_article
        year_article = []
    return render_template('archives.html',
                           articles=articles,
                           year=year,
                           data=data,
                           count=count,
                           pagination=pagination, endpoint='.archives')