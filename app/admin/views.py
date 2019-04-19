import flask_admin as admin
from flask_admin import expose
from flask import  request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required
from app.form.login_register import AdminLoginForm
from app.models.auth import User
import flask_login as login
from wtforms import TextAreaField
from flask_admin.contrib import sqla


class MyView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = AdminLoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
            else:
                flash('账号不存在或密码错误')
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        # self._template_args['link'] = link
        return super(MyView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))



    # 用户信息
class UserAdmin(sqla.ModelView):
    column_list = ('nick_name', 'email')
    form_overrides = dict(about_me=TextAreaField)
    column_searchable_list = ('email', 'nick_name')
    column_labels = dict(
        email=('邮箱'),
        nick_name=('用户名'),
    )

    # 判断后面是否显示
    def is_accessible(self):
        return current_user.is_authenticated
