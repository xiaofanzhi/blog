from wtforms import Form,StringField,IntegerField,PasswordField
from wtforms.validators import Length, number_range, DataRequired, Email, ValidationError, EqualTo


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(),Length(3,64),Email(message='电子邮件格式错误')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(1, 128)])
    nick_name = StringField('昵称', validators=[DataRequired(), Length(1, 10, message='昵称至少需要两个字符，最多10个字符')])

class LoginForm(Form):
    nick_name = StringField(validators=[DataRequired(),Length(3,64)])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(1, 128)])

class AdminLoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(3, 64), Email(message='电子邮件格式错误')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(1, 128)])