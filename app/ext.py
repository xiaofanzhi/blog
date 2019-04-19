
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment



login_manager = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
db=SQLAlchemy()
