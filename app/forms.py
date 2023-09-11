from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length, ValidationError
from flask_bcrypt import check_password_hash

from models import Customer, Showing, Film


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        customers = Customer.query.all()

        if any(i.username == username.data for i in customers):
            raise ValidationError(message="Username is taken, please try a different one.")

    def validate_password(self, password):

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
    no_of_adult = IntegerField("Number of Adult tickets", validators=[DataRequired()])
    no_of_child = IntegerField("Number of Child tickets", validators=[DataRequired()])
    submit = SubmitField("Confirm Order")

    def validate_username(self, username):
        customers = Customer.query.all()

        if not any(i.username == username.data for i in customers):
            raise ValidationError(message="Username does not exist.")
    
    def validate_password(self, password):
        
        customer = Customer.query.filter_by(username=self.username.data).first()
        if customer:
            if not check_password_hash(customer.password, password.data):
                raise ValidationError(message="Password is Incorrect, please try again.")

    def validate_no_of_child(self, no_of_child):
        film = Film.query.filter_by(id=self.movie.data).first()
        show = Showing.query.filter_by(film_id=film.id,date=self.date.data,time=self.time.data).first()

        if show.tickets < (self.no_of_adult.data + no_of_child.data):
            raise ValidationError(message=f"Please select less tickets, only {show.tickets} are avaiable.")
        