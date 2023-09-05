from app import app, bcrypt
from models import *

actor = Actor(first_name="John", last_name="actor")
film = Film(title="My first film.")
customer = Customer(username="John Buyer", password="Password")
transaction = Transaction(customer=customer)


film.actors.append(actor)


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([actor, film, customer, transaction])


if __name__ == "__main__":
    populate_db()
