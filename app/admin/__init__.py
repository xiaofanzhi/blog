from flask_admin import Admin
from app.admin.views import MyView,UserAdmin
from app.models.auth import User
from app.models.base import db

admin = Admin(name='后台管理系统',index_view=MyView(name='导航栏'),base_template='admin/my_master.html')
admin.add_view(UserAdmin(User, db.session, name='用户信息'))