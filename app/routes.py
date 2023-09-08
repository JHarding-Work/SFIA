from app import app, bcrypt
from app.models import *
from app.forms import *

from datetime import datetime, date, timedelta
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
    
    print(current_time)
    print(lb)
    print(ub)

    return render_template(
        'listings.html',
        films=Film.query.filter(lb < Film.release_date, Film.release_date<ub).all(),
        form=form
    )


@app.route('/ticket booking', methods=['GET', 'POST'])
def ticket_booking():
    form = BookingForm()

    films_list = Film.query.all()
    form.movie.choices = [(i.id, i.title) for i in films_list]

    if form.search.data:
        showing_list = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data).all()
        form.time.choices = [(i.time,i.time) for i in showing_list]

        return render_template('ticket_booking.html',form=form)
    
    elif form.submit.data:
        adult_ticket = form.no_of_adult.data
        child_ticket = form.no_of_child.data
        showingbackref = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data, time=form.time.data).first()
   
        if Customer.query.filter_by(username=form.username.data).count() == 1:
            customer = Customer.query.filter_by(username=form.username.data).first()

            if bcrypt.check_password_hash(customer.password, form.password.data):
                
                new_transaction = Transaction(customer=customer.id)  
                db.session.add(new_transaction)
                db.session.commit()
                
                new_booking = Booking(
                    child_ticket=child_ticket,
                    adult_ticket=adult_ticket,
                    transaction=new_transaction,
                    showing=showingbackref
                )
                db.session.add(new_booking)

    return render_template('ticket_booking.html',form=form)
