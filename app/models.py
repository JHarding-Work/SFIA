from app import db


actor_film = db.Table(
    "actor_film",
    db.metadata,
    db.Column("actor_id", db.ForeignKey("actor.id")),
    db.Column("film_id", db.ForeignKey("film.id"))
)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    films = db.relationship("Film", secondary="actor_film", back_populates="actors")


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.Text)
    actors = db.relationship("Actor", secondary="actor_film", back_populates="films")


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address_line = db.Column(db.String(30))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(8))
    customer = db.relationship('Transaction', backref="customer")


class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cust_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
    booking = db.relationship('Booking',backref='transactionbr')