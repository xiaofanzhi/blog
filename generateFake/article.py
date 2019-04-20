from random import randint,seed
from sqlalchemy.exc import IntegrityError
from faker import Faker

from app import creat_app
from app.ext import db
from app.models.article import Article
from app.models.auth import User
import forgery_py
fake=Faker()
def article(count=100):
    with creat_app().app_context():
        user_count = User.query.count()
        for i in range(count):
            u = User.query.first()
            c = u.id
            p=Article(
                title = forgery_py.lorem_ipsum.title(),
                content=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                summary = forgery_py.lorem_ipsum.sentences(randint(1, 2)),
                created = forgery_py.date.date(True),
                # author_name = u.nick_name,
                author_id = u.id
            )

            db.session.add(p)
            print('成功')
        try:
            db.session.commit()
        except:
            print('错误，回滚')
            db.session.rollback()

if __name__ == '__main__':
    article(100)