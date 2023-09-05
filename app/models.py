from app import db


# Models go here.
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address_line = db.Column(db.String(30))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(8))
    customer = db.relationship('Transaction',backref="customerbr")

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cust_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
    booking = db.relationship('Booking',backref='transactionbr')