"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 12:08 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 12:08 PM
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 20)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')


class SigninForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 20)])
    email = StringField('email', validators=[Email()])
