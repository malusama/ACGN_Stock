from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class Register(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])


class Buy_stock(FlaskForm):
    num = StringField('Buy stock number', validators=[DataRequired()])
