from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Login_Form(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')