from app import app, bcrypt
from app.models import *
from app.forms import *

from flask import redirect, url_for, render_template, request


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login_Form()
    return render_template('login.html',form=form)


@app.route('/listings')
def listings():
    return render_template('listings.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/new_releases')
def new_releases():
    return render_template('new_releases.html')


@app.route('/ticket_booking')
def ticket_booking():
    return render_template('ticket_booking.html')


#if __name__ == "__main__":
#    app.run(debug=True)