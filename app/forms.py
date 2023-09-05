from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign up')


class DateSelectForm(FlaskForm):
    date = DateField("Date")
    submit = SubmitField("Find")