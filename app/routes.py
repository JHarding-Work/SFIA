from app import app, bcrypt, db
from models import *
from forms import *

from datetime import datetime, timedelta, time
from flask import render_template, request


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    message = None

    if request.method == 'POST':
        customer = Customer.query.filter_by(username=form.username.data).first()

        if customer and customer.check_password(form.password.data):
            message = "Logged In"
        else:
            message = "Failed to Log In"

    return render_template('login.html', form=form, message=message)


@app.route('/sign up', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            customer = Customer(
                username=form.username.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            db.session.add(customer)
            db.session.commit()
        else:
            print(form.errors)

    return render_template('sign_up.html', form=form)


@app.route('/opening times')
def opening_times():
    return render_template('opening_times.html')


@app.route('/listings', methods=['GET', 'POST'])
def listings():
    form = DateSelectForm()

    if not form.is_submitted():
        form.date.data = datetime.now().date()

    return render_template(
        'listings.html',
        films=Film.query.all(),
        form=form,
    )


@app.route('/film/<int:film_id>')
def film(film_id):
    return render_template("film.html", film=Film.query.get(film_id))


@app.route('/about us')
def about_us():
    return render_template('about_us.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    return render_template('contacts.html')


@app.route('/new releases')
def new_releases():
    form = DateSelectForm()

    if not form.is_submitted():
        form.date.data = datetime.now().date()
    
    current_time = datetime.now()
    one_month = timedelta(days=30)

    lb = current_time - one_month
    ub = current_time + one_month

    return render_template(
        'listings.html',
        films=Film.query.filter(lb < Film.release_date, Film.release_date<ub).all(),
        form=form
    )


@app.route('/ticket booking', methods=['GET', 'POST'])
def ticket_booking():
    form = BookingForm(request.form)

    films_list = Film.query.all()
    form.movie.choices = [(i.id, i.title) for i in films_list]

    if form.submit.data:
        showing_list = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data).all()
        form.time.choices = [(i.time, i.time) for i in showing_list]

        if form.validate_on_submit():
            adult_ticket = form.no_of_adult.data
            child_ticket = form.no_of_child.data

            showing_time = time(*map(int, form.time.data.split(':')))
            showing = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data, time=showing_time).first()

            customer = Customer.query.filter_by(username=form.username.data).first()

            if customer and customer.check_password(form.password.data):
                new_transaction = Transaction(customer=customer)
                db.session.add(new_transaction)
                db.session.commit()

                new_booking = Booking(
                    child_ticket=child_ticket,
                    adult_ticket=adult_ticket,
                    transaction=new_transaction,
                    showing=showing
                )
                db.session.add(new_booking)
                db.session.commit()

    elif form.search.data:
        showing_list = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data).all()
        form.time.choices = [(i.time,i.time) for i in showing_list]

    return render_template('ticket_booking.html',form=form)
