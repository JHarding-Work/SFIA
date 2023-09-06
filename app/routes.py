from app import app, bcrypt
from app.models import *
from app.forms import *

from datetime import datetime
from flask import redirect, url_for, render_template, request


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if Customer.query.filter_by(username=form.username.data).count() == 1:
            customer = Customer.query.filter_by(username=form.username.data).first()

            if bcrypt.check_password_hash(customer.password, form.password.data):
                print("logged in")
        else:
            print("Failed to login")

    return render_template('login.html', form=form)


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

    return render_template('login.html', form=form)


@app.route('/opening times')
def opening_times():
    return render_template('opening_times.html')


@app.route('/listings', methods=['GET', 'POST'])
def listings():
    form = DateSelectForm()
    target_date = form.date.data if form.is_submitted() else datetime.now().date()

    return render_template(
        'listings.html',
        films=Film.query.all(),
        form=form,
        date=target_date,
    )


@app.route('/about us')
def about_us():
    return render_template('about_us.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/new releases')
def new_releases():
    return render_template('new_releases.html')


@app.route('/ticket booking')
def ticket_booking():
    return render_template('ticket_booking.html')
