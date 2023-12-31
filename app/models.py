from typing import List

from app import db, bcrypt

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
    def fullname(self) -> str:
        """
        Returns the first and last names of a Person in one word.
        """
        return f"{self.first_name} {self.last_name}"


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    release_date = db.Column(db.Date)
    description = db.Column(db.Text)
    image_src = db.Column(db.String(30), default="")
    director_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    actors = db.relationship("Person", secondary="actor_film", back_populates="starred_in")
    showings = db.relationship("Showing", backref="film")

    def next_showing(self):
        if self.showings:
            return min(showing.date for showing in self.showings)

        return None

    @property
    def actor_list(self) -> List[str]:
        """
        Returns a list of the full names of all actors for the film.
        """
        return [actor.fullname for actor in self.actors]


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address_line = db.Column(db.String(30))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(8))
    card_name = db.Column(db.String(20))
    card_no = db.Column(db.String(16))
    card_exp = db.Column(db.String(7))
    cvv = db.Column(db.String(3))
    transactions = db.relationship("Transaction", backref="customer")

    def check_password(self, password: str) -> bool:
        """
        Compares a given password against the hash stored, returning true if the hash matches.
        """
        return bcrypt.check_password_hash(self.password, password)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_complete = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    bookings = db.relationship("Booking", backref="transaction")


class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    tickets = db.Column(db.Integer, default=0)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    bookings = db.relationship("Booking", backref="showing")

    @property
    def formatted_time(self) -> str:
        """
        The time, rendered in %H:%m format, where minutes are always shown in double decimal figures.
        """
        return f"{self.time.hour}:{self.time.minute:0<2}"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_ticket = db.Column(db.Integer, default=0)
    adult_ticket = db.Column(db.Integer, default=0)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    showing_id = db.Column(db.Integer, db.ForeignKey('showing.id'), nullable=False)
    