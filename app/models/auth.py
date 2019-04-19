from app.models.base import Base
from flask_login import UserMixin
from sqlalchemy import Column,Integer,String,Text
from werkzeug.security import generate_password_hash,check_password_hash



class User(UserMixin,Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String(64), nullable=False)
    email = Column(String(51), unique=True, nullable=False)
    _password = Column('password', String(500))



    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)