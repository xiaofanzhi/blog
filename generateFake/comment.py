from random import randint,seed
from sqlalchemy.exc import IntegrityError
from faker import Faker

from app import creat_app
from app.ext import db
from app.models.article import Article,Comment
from app.models.auth import User
import forgery_py
fake=Faker()

def Article_comment(count=100):
    with creat_app().app_context():
        seed()
        artcile_count = Article.query.count()
        for i in range(count):
            a = Article.query.offset(randint(0,artcile_count-1)).first()
            c = Comment(content=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                        created=forgery_py.date.date(True),
                        commenter_name=forgery_py.internet.user_name(True),
                        commenter_email=forgery_py.internet.email_address(),
                        article_id=a.id
                        )
            db.session.add(c)
            print('成功')
        try:
            db.session.commit()
        except:
            print('错误，回滚')
            db.session.rollback()


if __name__ == '__main__':
    Article_comment(30)