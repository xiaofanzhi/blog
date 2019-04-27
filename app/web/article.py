from app.form.comment_form import CommentForm
from . import web
from flask import current_app, abort
from flask import render_template,request,url_for,redirect
from app.models.article import Article, Comment, Follow
from app.ext import db



@web.route('/')
def index():
    x  =request
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

    form = CommentForm(request.form, follow_id=-1)


    if form.validate_on_submit():
        followed_id = int(form.follow_id.data if form.follow_id.data else -1)
        reply_to = form.follow.data
        content = form.content.data
        if reply_to:
            content = form.content.data.replace("@" + reply_to + " ", "")
        comment = Comment(article=article,
                          content=content,
                          commenter_name=form.name.data,
                          commenter_email=form.email.data)
        db.session.add(comment)
        db.session.commit()

        if followed_id != -1:
            followed = Comment.query.get_or_404(followed_id)
            f = Follow(follower=comment, followed=followed)
            comment.comment_type = 'reply'
            # comment.reply_to = followed.author_name
            comment.reply_to = reply_to if reply_to else followed.commenter_name
            db.session.add(f)
            db.session.add(comment)
            db.session.commit()
        # flash(u'提交评论成功！', 'success')
        # if form.errors:
        #     flash(u'发表评论失败', 'danger')
        return redirect(url_for('.article', id=article.id, page=-1))


    page = request.args.get('page', 1, type=int)
    counts = article.comments.count()
    if page == -1:
        page = int((counts - 1) / current_app.config['COMMENT_PER_PAGE'] + 1)
    pagination = article.comments.order_by(Comment.created.asc()).paginate(
        page,per_page=current_app.config['COMMENT_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return  render_template('article.html', article=article, category_id=article.category_id, next_article=next,
                           prev_article=prev, comments=comments, counts=counts, pagination=pagination, form=form,
                           endpoint='.article', id=article.id)

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



@web.route('/search/')
def search():
    page = int(request.args.get('page',1))
    keyword = request.args.get('keyword',None)
    pagination = None
    articles = None
    if keyword:
        pagination = Article.query.search(keyword).order_by(
            Article.created.desc()).paginate(
                page,per_page=current_app.config['PER_PAGE'],
                error_out=False)
        articles = pagination.items

    return render_template('index.html',
                           articles=articles,
                           keyword=keyword,
                           pagination=pagination, endpoint='.index')