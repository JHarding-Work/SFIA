from datetime import time, datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length, ValidationError
from re import match
from models import Customer, Showing


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username) -> None:
        customers = Customer.query.all()

        if any(i.username == username.data for i in customers):
            raise ValidationError(message="Username is taken, please try a different one.")

    def validate_password(self, password) -> None:

            special_char = ['!','£','$','%','^','&','*','(',')',';',':']
            digits = list(i for i in range(0,10))
            print(password.data)
            if len(password.data) < 8:
                raise ValidationError(message="Password must be at least 8 characters long")

            elif not any(i in password.data for i in special_char):
                raise ValidationError(message=f"Password must include one special character from {special_char}")
            elif not any(str(i) in password.data for i in digits):
                raise ValidationError(message="Password must include at least one number")


class DateSelectForm(FlaskForm):
    date = DateField("Date")
    submit = SubmitField("Find")


class BookingForm(FlaskForm):
    movie = SelectField("Movie: ", validators=[DataRequired()])
    search = SubmitField("Search")
    date = DateField("Date", validators=[DataRequired()])
    time = SelectField("Times: ", validators=[DataRequired()])
    username = StringField("Username: ", validators=[DataRequired()])
    password = StringField("Password: ", validators=[DataRequired()])
    no_of_adult = IntegerField("Number of Adult tickets", validators=[])
    no_of_child = IntegerField("Number of Child tickets", validators=[])
    submit = SubmitField("Confirm Order")

    @property
    def dt_time(self) -> time:
        return time(*map(int, self.time.data.split(':')))

    def validate_username(self, username) -> None:
        customers = Customer.query.all()

        if not any(i.username == username.data for i in customers):
            raise ValidationError(message="Username does not exist.")
    
    def validate_password(self, password) -> None:
        customer = Customer.query.filter_by(username=self.username.data).first()

        if customer and not customer.check_password(password.data):
            raise ValidationError(message="Password is Incorrect, please try again.")

    def validate_no_of_child(self, no_of_child) -> None:
        show = Showing.query.filter_by(
            film_id=self.movie.data,
            date=self.date.data,
            time=self.dt_time
        ).first()

        if show.tickets < (self.no_of_adult.data + no_of_child.data):
            raise ValidationError(message=f"Please select less tickets, only {show.tickets} are avaiable.")
        

class PaymentForm(FlaskForm):
    address_line = StringField('Address: ', validators=[DataRequired(),Length(max=30)])
    city = StringField('City: ', validators=[DataRequired(),Length(max=30)])
    postcode = StringField('Postcode: ', validators=[DataRequired(),Length(max=8)])
    card_name = StringField('Card Name:', validators=[DataRequired(),Length(max=20)])
    card_no = StringField('Card Number:', validators=[DataRequired(),Length(min=16,max=16)])
    card_exp = StringField('Card Expiration Date:', validators=[DataRequired(),Length(max=7)])
    cvv = StringField('cvv', validators=[DataRequired(), Length(min=3,max=3)])
    submit = SubmitField('Finalise Puchase')

    def validate_postcode(self, postcode) -> None:
        pattern = r'\A([A-Za-z]){2}(\d){1,2}(\s)?(\d)([A-Za-z]){2}\Z'
        if not match(pattern, postcode.data):
            raise ValidationError(message='Please enter the postcode in the following format: "AB1 2CD" or "AB12 3CD"')

    def validate_card_no(self, card_no) -> None:
                
        if not all(i.isdigit() for i in card_no.data):
            raise ValidationError(message='Please ensure you only use numerical characters.')
        
    def validate_card_exp(self, card_exp) -> None:
        pattern = r'\A(\d){2}(/)(\d){4}\Z'
        today = datetime.now().date()

        if not match(pattern, card_exp.data):
            raise ValidationError(message='Please put the date in the following format: mm/yyyy (eg: 09/2026 for September 2026).')
        elif int(''.join(card_exp.data[0:2])) > 12:
            raise ValidationError(message='please input a valid month between 01 and 12')
        elif today.year > int(''.join(card_exp.data[3:7])) or (today.year == int(''.join(card_exp.data[3:7])) and today.month > int(''.join(card_exp.data[0:2]))):
            raise ValidationError(message='Your card seems to have expired, please check the expiration date.')
        
    def validate_cvv(self, cvv) -> None:
       if not all(i.isdigit() for i in cvv.data):
            raise ValidationError(message='please ensure the cvv only includes numerical values.')