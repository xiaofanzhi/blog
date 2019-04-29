from . import web
from app.form.login_register import RegisterForm,LoginForm
from flask import render_template,request,url_for,redirect,flash
from app.models.auth import User
from app.ext import db

from flask_login import login_user


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nick_name = form.nick_name.data).first()
        # 比对密码
        if user and user.check_password(form.password.data):
            login_user(user,remember=True)
            # next = request.args.get('next')
            # if not next or not next.startswith('/'):
            #     next = url_for('web.index')
            # return redirect(next)
            return '成功'
        else:
            flash('账号不存在或密码错误')
    return render_template('signin.html',form=form)


# @web.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        # redirect 需要endpoint
        return redirect(url_for('web.login'))
    return render_template('signup.html',form=form)