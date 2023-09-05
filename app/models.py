from app import db


actor_film = db.Table(
    "actor_film",
    db.metadata,
    db.Column("actor_id", db.ForeignKey("actor.id")),
    db.Column("film_id", db.ForeignKey("film.id"))
)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20) nullable=False)
    last_name = db.Column(db.String(20))
    films = db.relationship("Film", secondary="actor_film", back_populates="actors")


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    actors = db.relationship("Actor", secondary="actor_film", back_populates="films")
    showings = db.relationship("Showing", backref="film")


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address_line = db.Column(db.String(30))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(8))
    transactions = db.relationship("Transaction", backref="customer")


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    film_id = db.column(db.Integer, db.ForeignKey('film.id'), nullable=False)