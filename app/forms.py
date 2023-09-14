from datetime import time, datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_bcrypt import check_password_hash
from re import match
from models import Customer, Showing, Film


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """Ensures the username doesn't already exist in the Customer table"""
        customers = Customer.query.all()

        if any(i.username == username.data for i in customers):
            raise ValidationError(message="Username is taken, please try a different one.")

    def validate_password(self, password):
        """Checks the password for at least one special character and one numerical value"""
        special_char = {'!', '£', '$', '%', '^', '&', '*', '(', ')', ';', ':'}
        digits = set(map(str, range(10)))
        password_characters = set(password.data)

        if not password_characters & special_char:
            raise ValidationError(message=f"Password must include one special character from {special_char}")
        if not password_characters & digits:
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
    def dt_time(self):
        return time(*map(int, self.time.data.split(':')))

    def validate_username(self, username):
        """Checks that a customer exists with a matching username"""
        customers = Customer.query.all()

        if not any(i.username == username.data for i in customers):
            raise ValidationError(message="Username does not exist.")

    def validate_password(self, password):
        """Checks for a password match from the record based on the existing username"""
        customer = Customer.query.filter_by(username=self.username.data).first()
        if customer:
            if not check_password_hash(customer.password, password.data):
                raise ValidationError(message="Password is Incorrect, please try again.")

    def validate_no_of_child(self, no_of_child):
        """Checks the amount of tickets avaiable is more than the amount attempting to be booked"""
        show = Showing.query.filter_by(
            film_id=self.movie.data,
            date=self.date.data,
            time=self.dt_time
        ).first()

        if show.tickets < (self.no_of_adult.data + no_of_child.data):
            raise ValidationError(message=f"Please select less tickets, only {show.tickets} are avaiable.")


class PaymentForm(FlaskForm):
    address_line = StringField('Address: ', validators=[DataRequired(), Length(max=30)])
    city = StringField('City: ', validators=[DataRequired(), Length(max=30)])
    postcode = StringField('Postcode: ', validators=[DataRequired(), Length(max=8)])
    card_name = StringField('Card Name:', validators=[DataRequired(), Length(max=20)])
    card_no = StringField('Card Number:', validators=[DataRequired(), Length(min=16, max=16)])
    card_exp = StringField('Card Expiration Date:', validators=[DataRequired(), Length(max=7)])
    cvv = StringField('cvv', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Finalise Puchase')

    def validate_postcode(self, postcode):
        """Checks the formatting of the Postcode"""
        pattern = r'\A([A-Za-z]){2}(\d){1,2}(\s)?(\d)([A-Za-z]){2}\Z'
        if not match(pattern, postcode.data):
            raise ValidationError(message='Please enter the postcode in the following format: "AB1 2CD" or "AB12 3CD"')

    def validate_card_no(self, card_no):
        """Ensures all inputted values in the card number are numerical"""
        if not all(i.isdigit() for i in card_no.data):
            raise ValidationError(message='Please ensure you only use numerical characters.')

    def validate_card_exp(self, card_exp):
        """Checks the formatting of the Card expiry, that the month is between 1 and 12 and that the card isn't past
        the expiration date"""
        pattern = r'\A(\d){2}(/)(\d){4}\Z'
        today = datetime.now().date()

        if not match(pattern, card_exp.data):
            raise ValidationError(
                message='Please put the date in the following format: mm/yyyy (eg: 09/2026 for September 2026).')
        elif int(''.join(card_exp.data[0:2])) > 12:
            raise ValidationError(message='please input a valid month between 01 and 12')
        elif today.year > int(''.join(card_exp.data[3:7])) or (
                today.year == int(''.join(card_exp.data[3:7])) and today.month > int(''.join(card_exp.data[0:2]))):
            raise ValidationError(message='Your card seems to have expired, please check the expiration date.')

    def validate_cvv(self, cvv):
        """Ensures all inputted values in the cvv are numerical"""
        if not all(i.isdigit() for i in cvv.data):
            raise ValidationError(message='please ensure the cvv only includes numerical values.')


class Searchform(FlaskForm):
    search = StringField(default=str())
    submit = SubmitField("Search")
