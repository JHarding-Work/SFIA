from werkzeug import Response

from app import app, bcrypt, db
from models import *
from forms import *

from datetime import datetime, timedelta, time
from flask import redirect,render_template, request


@app.route('/')
@app.route('/home')
def home() -> str:
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login() -> str:
    form = LoginForm()
    message = None

    if request.method == 'POST':
        customer = Customer.query.filter_by(username=form.username.data).first()

        if customer and customer.check_password(form.password.data):
            message = "Logged In"
        else:
            message = "Failed to Log In"

    return render_template('login.html', form=form, message=message)


@app.route('/signup', methods=["GET", "POST"])
def signup() -> str:
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


@app.route('/opening')
def opening_times() -> str:
    return render_template('opening_times.html')


@app.route('/listings', methods=['GET', 'POST'])
def listings() -> str:
    form = Searchform()

    return render_template(
        'listings.html',
        form=form,
        films=Film.query.filter(Film.title.contains(form.search.data)),
        title="All Showings"
    )


@app.route('/film/<int:film_id>', methods=['GET', 'POST'])
def film(film_id) -> str:
    target_film = Film.query.get(film_id)
    form = DateSelectForm()

    if not form.is_submitted():
        now = datetime.now().date()
        next_showing = target_film.next_showing()

        form.date.data = max(next_showing, now) if next_showing else now

    return render_template(
        "film.html",
        film=target_film,
        form=form
    )


@app.route('/about')
def about_us() -> str:
    return render_template('about_us.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts() -> str:
    return render_template('contacts.html')


@app.route('/new', methods=['GET', 'POST'])
def new_releases() -> str:
    form = Searchform()

    current_time = datetime.now()
    one_month = timedelta(days=30)

    lb = current_time - one_month
    ub = current_time + one_month
    films = Film.query.filter(
        lb < Film.release_date, Film.release_date < ub
    ).filter(
        Film.title.contains(form.search.data)
    )

    return render_template('listings.html', form=form, films=films, title="New Releases")


@app.route('/bookings', methods=['GET', 'POST'])
def ticket_booking() -> Response | str:
    form = BookingForm(request.form)

    films_list = Film.query.all()
    form.movie.choices = [(i.id, i.title) for i in films_list]

    if form.submit.data:
        showing_list = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data).all()
        form.time.choices = [(i.time, i.time) for i in showing_list]

        if form.validate_on_submit():
            adult_ticket = form.no_of_adult.data
            child_ticket = form.no_of_child.data

            showing = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data, time=form.dt_time).first()
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
                return redirect(f'/payments/{customer.id}/{new_transaction.id}')

    elif form.search.data:
        showing_list = Showing.query.filter_by(film_id=form.movie.data, date=form.date.data).all()
        form.time.choices = [(i.time,i.time) for i in showing_list]

    return render_template('ticket_booking.html', form=form)


@app.route('/payments/<int:cust_id>/<int:trans_id>', methods=['GET', 'POST'])
def payments(cust_id, trans_id) -> Response | str:
    form = PaymentForm()

    if form.validate_on_submit():
        customer = Customer.query.filter_by(id=cust_id).first()
        customer.address_line = form.address_line.data
        customer.city = form.city.data
        customer.postcode = form.postcode.data
        customer.card_name = form.card_name.data
        customer.card_no = form.card_no.data
        customer.card_exp = form.card_exp.data
        customer.cvv = form.cvv.data
        transaction = Transaction.query.filter_by(id=trans_id).first()
        transaction.is_complete = True
        db.session.commit()
        return redirect('/success')

    return render_template('payments.html', form=form)


@app.route('/success')
def pay_success() -> str:
    return render_template('pay_success.html')
