import hashlib
from functools import reduce

import bleach
from flask_sqlalchemy import BaseQuery
from markdown import markdown
from sqlalchemy.orm import relationship

from app.models.base import Base
from flask import request, url_for
from sqlalchemy import Column, Integer, String, Text, Boolean,DateTime,ForeignKey,Table
import re
from app.ext import db, keywords_split
from .auth import User
from datetime import datetime
from jinja2.filters import do_striptags, do_truncate
pattern_hasmore = re.compile(r'<!--more-->', re.I)

def markitup(text):
    """
    把Markdown转换为HTML
    """

    # 删除与段落相关的标签，只留下格式化字符的标签
    # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #                 'h1', 'h2', 'h3', 'p', 'img']
    return bleach.linkify(markdown(text, ['extra'], output_format='html5'))
    # return bleach.linkify(bleach.clean(
    #     # markdown默认不识别三个反引号的code-block，需开启扩展
    #     markdown(text, ['extra'], output_format='html5'),
    #     tags=allowed_tags, strip=True))


# 类别
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True)
    order = Column(Integer)
    name = Column(String(128),unique=True)
    parent_id = Column(Integer(), ForeignKey('categories.id'))
    # parent = db.relationship('Category',
    #                          primaryjoin='Category.parent_id == Category.id',
    #                          remote_side=id, backref=db.backref("children"))
    introduction = Column(Text, default=None)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    # 设置默认排序使用
    __mapper_args__ = {'order_by': [name]}
    # 用于在主页面点击类别 定位到那个类别

    @property
    def link(self):
        return url_for('web.category', id=self.id, _external=True)

    @property
    def count(self):
        ls =db.session.query(Category.id).all()
        cate_ids = [cate_id for cate_id in ls]
        return Article.query.public().filter(Article.category_id.in_(cate_ids)).count()


    def __repr__(self):
        return '<Category %r>' % self.name

    def __str__(self):
        return self.name


class Tag(Base):
    """标签"""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

    __mapper_args__ = {'order_by': [id.desc()]}

    @property
    def link(self):
        return url_for('web.tag', name=self.name.lower(), _external=True)

    @property
    def count(self):
        return Article.query.public().filter(Article.tags.any(id=self.id)).count()

    def __repr__(self):
        return '<Tag %r>' % self.name

    def __str__(self):
        return self.name

# Create M2M table
# 多对多中间那张表
article_tags_table = Table('article_tags',
                            Base.metadata,
                            Column('article_id', Integer(), ForeignKey('articles.id')),
                            Column('tag_id', Integer(), ForeignKey('tags.id')))



class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(128),unique=True)
    articles = relationship('Article', backref='source', lazy='dynamic')

    @staticmethod
    def insert_sources():
        sources= ('原创','转载','翻译')
        for i in sources:
            source = Source.query.filter_by(name=i).first()
            if source is None:
                source = Source(name=i)
            db.session.add(source)
        db.session.commit()

    __mapper_args__ = {'order_by': [name]}

    @property
    def link(self):
        return url_for('web.source', id=self.id, _external=True)

    @property
    def count(self):
        return Article.query.public().filter(Article.source_id.in_(id=self.id)).count()



    def __repr__(self):
        return '<Source %r>' % self.name

    def __str__(self):
        return self.name




class ArticleQuery(BaseQuery):

    def search(self, keyword):
        criteria = []

        for keyword in keywords_split(keyword):
            keyword = u'%{0}%'.format(keyword)
            criteria.append(db.or_(Article.title.ilike(keyword), ))

        q = reduce(db.or_, criteria)
        return self.filter_by(published=True).filter(q)
# 判断是否有人回复？？？
class Follow(Base):
    __tablename__ = 'follows'
    follower_id = Column(Integer, ForeignKey('comments.id'),
                            primary_key=True)
    followed_id = Column(Integer, ForeignKey('comments.id'),
                            primary_key=True)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer,primary_key=True)
    content = Column(Text)
    created = Column(DateTime, default=datetime.now)
    commenter_name = Column(String(64))
    commenter_email = Column(String(64))
    # 头像相关
    avatar_hash = Column(String(32))

    article_id = Column(Integer,ForeignKey('articles.id'))
    disabled = Column(Boolean, default=False)
    comment_type = Column(db.String(64), default='comment')
    reply_to = Column(String(128), default='notReply')


    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    @property
    def replys(self):
        return [i.follower for i in self.followers]



    # 根据email 生成图像
    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.commenter_email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.commenter_email.encode('utf-8')).hexdigest()



    def gravatar(self, size=40, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.commenter_email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


    def followed_name(self):
        if self.is_reply():
            return self.followed.first().followed.commenter_name


    def __repr__(self):
        return '<Comment %r>' % self.id

    def __str__(self):
        return self.id



class Article(Base):
    __tablename__ = 'articles'
    query_class = ArticleQuery
    # per_page = current_app.config['PER_PAGE']

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(256),index=True)
    summary = Column(Text)
    published = Column(Boolean, default=True)

    hits = Column(Integer, default=0)

    content = Column(Text)
    content_html = Column(Text)
    created = Column(DateTime())
    last_modified = Column(DateTime())

    author_id = Column(Integer, ForeignKey(User.id))

    tags = relationship(Tag, secondary=article_tags_table, backref=db.backref("articles"))
    category_id = Column(Integer(), ForeignKey(Category.id), nullable=False)
    source_id = Column(Integer, ForeignKey(Source.id), nullable=False, )
    comments = db.relationship('Comment', backref='article', lazy='dynamic')


    def __repr__(self):
        return '<Article %r>' % (self.title)

    def __str__(self):
        return self.title\


    @property
    def year(self):
        return int(self.created.year)

    @property
    def month_and_day(self):
        return str(self.created.month) + "-" + str(self.created.day)

    @property
    def link(self):
        return url_for('web.article',id=self.id, _external=True)

    @property
    def month_and_day(self):
        return str(self.created.month) + "-" + str(self.created.day)

    @property
    def get_next(self):
        pass

    @property
    def get_prev(self):
        pass

    @property
    def has_more(self):
        return pattern_hasmore.search(self.body) is not None or \
               self.summary.find('...') >= 0

    @staticmethod
    def on_change_content(target, value, oldvalue, initiator):
        target.content_html = markitup(value)

        # TODO 有问题
        def _format(_html):
            return do_truncate(do_striptags(_html), length=200)

        if target.summary is None or target.summary.strip() == '':
            # 新增文章时，如果 summary 为空，则自动生成

            _match = pattern_hasmore.search(value)
            if _match is not None:
                more_start = _match.start()
                # target.summary = _format(markitup(value[:more_start]))
                target.summary = markitup(value[:more_start])
            else:
                target.summary = target.body_html

    @staticmethod
    def before_insert(mapper, connection, target):
        def _format(_html):
            return do_truncate(do_striptags(_html), length=200)

        value = target.content
        if target.summary is None or target.summary.strip() == '':
            # 新增文章时，如果 summary 为空，则自动生成

            _match = pattern_hasmore.search(value)
            if _match is not None:
                more_start = _match.start()
                target.summary = _format(markitup(value[:more_start]))
            else:
                target.summary = _format(target.body_html)

db.event.listen(Article.content, 'set', Article.on_change_content)
db.event.listen(Article, 'before_insert', Article.before_insert)











