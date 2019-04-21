from app.models.base import Base
from flask import current_app, request, url_for
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, Boolean,DateTime
import re
from  app.ext import db
from .auth import User
from datetime import datetime

pattern_hasmore = re.compile(r'<!--more-->', re.I)





class Article(Base):
    __tablename__ = 'articles'

    # per_page = current_app.config['PER_PAGE']

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(128),index=True)
    summary = Column(Text)
    published = Column(Boolean, default=True)

    hits = Column(Integer, default=0)

    content = Column(Text)
    content_html = Column(Text)
    created = Column(DateTime())
    last_modified = Column(DateTime())

    author_id = Column(Integer, db.ForeignKey(User.id))


    # def __init__(self):
    #     self.created = int(datetime.now().timestamp())



    def __repr__(self):
        return '<Article %r>' % (self.title)

    def __str__(self):
        return self.title

    @property
    def link(self):
        # return url_for('web.article', id=self.id, _external=True)
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

    # @staticmethod
    # def on_change_content(target, value, oldvalue, initiator):
    #     target.content_html = markitup(value)
    #
    #     # TODO 有问题
    #     def _format(_html):
    #         return do_truncate(do_striptags(_html), length=200)
    #
    #     if target.summary is None or target.summary.strip() == '':
    #         # 新增文章时，如果 summary 为空，则自动生成
    #
    #         _match = pattern_hasmore.search(value)
    #         if _match is not None:
    #             more_start = _match.start()
    #             # target.summary = _format(markitup(value[:more_start]))
    #             target.summary = markitup(value[:more_start])
    #         else:
    #             target.summary = target.body_html