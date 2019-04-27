from . import web
from app.form.comment_form import CommentForm
from flask import current_app
from flask import render_template,request
from app.models.article import Follow,Comment
from app.ext import db

@web.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = CommentForm(request.form,follow_id=-1)
    if form.validate_on_submit():
        followed_id = int(form.follow_id.data if form.follow_id.data else -1)
        reply_to = form.follow.data
        content = form.content.data
        if reply_to:
            content = form.content.data.replace("@" + reply_to + " ", "")
        comment = Comment(content=content,
                          commenter_name=form.name.data,
                          commenter_email=form.email.data,
                          comment_type='contact')
        db.session.add(comment)
        db.session.commit()
        # 回复
        if followed_id !=-1:
            followed = Comment.query.get_or_404(followed_id)
            f = Follow(follower=comment, followed=followed)
            comment.comment_type = 'reply'
            comment.reply_to = reply_to if reply_to else followed.author_name
            db.session.add(f)
            db.session.add(comment)
            db.session.commit()
            # flash('提交评论成功！', 'success')
        # return redirect(url_for('.contact',page=-1))
    page = request.args.get('page', 1, type=int)
    _query = Comment.query.filter_by(comment_type='contact')
    counts = _query.count()
    if page == -1:
        page = int((counts - 1) / current_app.config['COMMENT_PER_PAGE'] + 1)
    pagination = _query.order_by(Comment.created.asc()).paginate(
        page, per_page=current_app.config['COMMENT_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('contact.html', comments=comments, counts=counts, pagination=pagination, form=form,
                           endpoint='.contact')