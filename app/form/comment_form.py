
from wtforms import Form,StringField,IntegerField,PasswordField, TextAreaField
from wtforms.validators import Length, number_range, DataRequired, Email
from flask_wtf import FlaskForm




class CommentForm(FlaskForm):
    name = StringField(u'昵称', validators=[DataRequired(), Length(1, 10, message='名字不能为空')])
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email(message='电子邮件格式错误')])
    content = TextAreaField(u'内容', validators=[DataRequired(), Length(1, 1024)])
    follow_id = StringField()
    follow = StringField()
