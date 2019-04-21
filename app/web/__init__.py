from flask import Blueprint

web=Blueprint('web',__name__)


from app.web import login_register
from app.web import article
from app.web import categorie
from app.admin.views import ArticleAdmin