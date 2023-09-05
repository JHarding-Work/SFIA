from app import db


actor_film = db.Table(
    "actor_film",
    db.metadata,
    db.Column("actor_id", db.ForeignKey("person.id")),
    db.Column("film_id", db.ForeignKey("film.id"))
)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    starred_in = db.relationship("Film", secondary="actor_film", back_populates="actors")
    directed = db.relationship("Film", backref="director")

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    release_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    image_src = db.Column(db.String(30), default="")
    director_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    actors = db.relationship("Person", secondary="actor_film", back_populates="starred_in")
    showings = db.relationship("Showing", backref="film")

    @property
    def actor_list(self):
        return [actor.fullname for actor in self.actors]


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
    bookings = db.relationship("Booking", backref="transaction")


class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    bookings = db.relationship("Booking", backref="showing")

    @property
    def formatted_time(self):
        return f"{self.datetime.hour}:{self.datetime.minute:0<2}"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_ticket = db.Column(db.Integer, default=0)
    adult_ticket = db.Column(db.Integer, default=0)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    showing_id = db.Column(db.Integer, db.ForeignKey('showing.id'), nullable=False)
    