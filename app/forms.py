from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from .models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session,current_app

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名只能由字母，数字，下划线和.构成，且必须以字母开始')])
    password = PasswordField('password',validators = [DataRequired(),Length(1,120)])
    remember_me = BooleanField('remember_me', default=False)
    recaptcha = StringField(u'recaptcha', validators=[DataRequired(message=u'验证码不能为空')])

    def validate_recaptcha(self, field):
        if session['S_RECAPTCHA'] != field.data.upper():
            raise ValidationError(u'验证码错误') 

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名只能由字母，数字，下划线和.构成，且必须以字母开始')])
    password = PasswordField('password',validators = [DataRequired(),Length(1,120)])
    repassword = PasswordField('repassword',validators = [DataRequired(),Length(1,120),EqualTo('password',message = u'两次输入不同')])
    email = StringField('email',validators = [DataRequired(),Length(1,64),Email()])


    def validate_username(self,field):
        if User.query.filter_by(username = str(field.data)).first():
            raise ValidationError('username already in use')

    def validate_email(self,field):
        if User.query.filter_by(email = str(field.data)).first():
            raise ValidationError('email has been used')


class RechangeForm(FlaskForm):
    newpassword = PasswordField('newpassword',validators = [DataRequired(),Length(1,120)])
    repassword = PasswordField('repassword',validators = [DataRequired(),Length(1,120),EqualTo('newpassword',message = u'两次输入不同')])

