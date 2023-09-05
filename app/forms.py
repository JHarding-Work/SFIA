from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField


class DateSelectForm(FlaskForm):
    date = DateField("Date")
    submit = SubmitField("Find")