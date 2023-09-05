from app import app, bcrypt
from app.models import *

from flask import redirect, url_for, render_template, request

@app.route('/')
@app.route('/Home')
def home():
    render_template('home.html')

@app.route('/Login')
def login():
    render_template('login.html')

@app.route('/Listings')
def listings():
    render_template('listings.html')

@app.route('/About us')
def about_us():
    render_template('about_us.html')

@app.route('/Contacts')
def contacts():
    render_template('contacts.html')

@app.route('/New Releases')
def new_releases():
    render_template('new_releases.html')

@app.route('/Ticket Booking')
def ticket_booking():
    render_template('ticket_booking.html')


if __name__ == "__main__":
    app.run(debug=True)