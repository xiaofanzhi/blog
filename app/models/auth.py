import bleach
from markdown import markdown

from app.models.base import Base
from flask import current_app, request
from flask_login import UserMixin
from sqlalchemy import Column,Integer,String,Text
from werkzeug.security import generate_password_hash,check_password_hash
from app import login_manager
import hashlib




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



class User(UserMixin,Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String(64), nullable=False)
    email = Column(String(51), unique=True, nullable=False)
    _password = Column('password', String(500))

    # admin用
    def is_authenticated(self):
        return True

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 使用登录限制 需要在这写个函数

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)






@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
