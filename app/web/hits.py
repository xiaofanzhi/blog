from app.models.article import Article
from . import web
from app.ext import db
from flask import request


@web.route('/get_hits/')
def get_hits():
    id = int(request.args.get('id',0))
    article = Article.query.get(id)
    if article:
        article.hits+=1
        db.session.add(article)
        db.session.commit()
        return str(article.hits)
    return '错误'