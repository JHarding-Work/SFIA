from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length,ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign up')

    ##### Fix this Later #####
    def validate_password(self, password):

            special_char = ['!','£','$','%','^','&','*','(',')',';',':']
            digits = list(i for i in range(0,10))

            for i in special_char:
                if not(i in password.data):
                    raise ValidationError(f"Password must include one special character from {special_char}")

            for i in digits:
                if not(digits in password.data):
                    raise ValidationError("Password must include at least one number")


class DateSelectForm(FlaskForm):
    date = DateField("Date")
    submit = SubmitField("Find")


class BookingForm(FlaskForm):
     movie = SelectField("Movie: ")
     date = DateField("Date")
     time = SelectField("Times: ")
     no_of_adults = IntegerField("Number of Adult tickets")
     no_of_child = IntegerField("Number of Child tickets")
     submit = SubmitField("Confirm Order")