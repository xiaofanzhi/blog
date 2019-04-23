from flask_admin import Admin
from app.admin.views import MyView,UserAdmin,ArticleAdmin,CategoryAdmin,TagAdmin,SourceAdmin
from app.models.auth import User
from app.models.article import Article,Category,Tag,Source
from app.models.base import db

admin = Admin(name='后台管理系统',index_view=MyView(name='导航栏'),base_template='admin/my_master.html')
admin.add_view(UserAdmin(User, db.session, name='用户信息'))
admin.add_view(ArticleAdmin(Article,db.session,name='文章列表'))
admin.add_view(CategoryAdmin(Category, db.session, name='分类'))
admin.add_view(TagAdmin(Tag,db.session,name='标签'))
admin.add_view(SourceAdmin(Source,db.session,name='文章来源'))