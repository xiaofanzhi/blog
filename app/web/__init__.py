from flask import Blueprint

web=Blueprint('web',__name__)


from app.web import login_register