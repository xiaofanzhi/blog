import os
import flask_admin as admin
from flask_admin import expose
from flask import  request, redirect, url_for, flash,current_app,Response
from flask_login import current_user, login_user
from werkzeug.utils import secure_filename

from app.admin.extras import allowed_photo, random_str,format_datetime
from app.form.login_register import AdminLoginForm

from app.models.auth import User
import flask_login as login
from wtforms import TextAreaField
from flask_admin.contrib import sqla
import json

import datetime

from app.web import web

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


# 文章
class ArticleAdmin(sqla.ModelView):
    create_template = "admin/model/a_create.html"
    edit_template = "admin/model/a_edit.html"

    column_list = ('title','published','hits','summary','created','last_modified')
    # 不想显示的字段
    form_excluded_columns = ('created','last_modified')

    column_exclude_list = ('title',)

    # 一个字典，格式化字段，定义字段的显示方式
    column_formatters = dict(created=format_datetime)

    form_create_rules = (
        'title', 'summary', 'published', 'content'
    )
    form_edit_rules = form_create_rules

    form_overrides = dict(
        summary=TextAreaField)

    column_labels = dict(
        title=('标题'),
        # category=('分类'),
        # source=('来源'),
        # tags=('标签'),
        content=('正文'),
        summary=('简介'),
        published=('是否已发布'),
        created=('创建时间'),
        hits=('阅读数'),
    )

    # @expose('/editor_pic',methods=['POST'])
    # def editor_pic(self):
    #     image_file =

    form_widget_args = {
        'title': {'style': 'width:480px;'},
        'summary': {'style': 'width:680px; height:80px;'},
    }

    # 判断后面是否显示
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/editor_pic', methods=["POST"])
    def editor_pic(self):
        image_file = request.files.get('editormd-image-file')
        if image_file and allowed_photo(image_file.filename):
            filename = secure_filename(image_file.filename)
            filename = str(datetime.date.today()) + '-' + random_str() + '-' + filename
            a = current_app.config['SAVEPIC']
            image_file.save(os.path.join(current_app.config['SAVEPIC'], filename))
            data= {
                'success': 1,
                'message': '图片上传成功',
                'url': url_for('web.image', name=filename)
                # 'url': '/upload'+filename
            }
        else:
            data = {
                'success': 0,
                'message': u'没有获得图片或图片类型不支',
                'url': ""
            }
        return json.dumps(data)

    # 如果之后前台显示不了图片 可能是这处理有问题@expose('/image/<name>')
    @web.route('/image/<name>')
    def image(name):
        with open(os.path.join(current_app.config['SAVEPIC'], name), 'rb') as f:
            # with open('app/admin/article/edit/'+name ,'rb') as f:
            resp = Response(f.read(), mimetype="image/jpeg")
        return resp


    # on_model_change(form,model,is_created)     在模板改变后需要做的事情  admin 定义好的
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.author_id = login.current_user.id
            model.created = datetime.datetime.now()
            model.last_modified = model.created
        else:
            model.last_modified = datetime.datetime.now()







