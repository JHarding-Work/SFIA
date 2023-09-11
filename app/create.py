from app import app, bcrypt
from models import *
from datetime import date, time
from time import sleep
from sqlalchemy.exc import OperationalError

john = Person(first_name="John", last_name="Actor")
sarah = Person(first_name="Sarah", last_name="Performer")
stephenson = Person(first_name="Stephen", last_name="Son")
louise = Person(first_name="Louise", last_name="Actor")
john_d = Person(first_name="John", last_name="Director")


oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg", release_date=date(2023,9,6))
blue = Film(title="Blue Beetle", director=sarah, actors=[stephenson], image_src="blue.jpg", release_date=date(2023,9,15))
lord_of_the_rings = Film(title="Lord of the Rings", director=john_d, actors=[john, sarah], image_src="lord-of-the-rings.jpg", release_date=date(2024,9,6))
toy = Film(title="Toy Story", actors=[john, louise], image_src="toy_story.jpg", release_date=date(2021,9,6))


for d in range(5, 14):
    for n in 11, 14:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer, tickets=123)


for d in range(13, 24):
    for n in 9, 13, 17:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer, tickets=32)

    for n in 11, 15:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=blue, tickets=12)


Showing(date=date(2023, 9, 25), time=time(11, 0), film=lord_of_the_rings)
Showing(date=date(2023, 9, 25), time=time(15, 0), film=toy)


customer = Customer(username="John Buyer", password=bcrypt.generate_password_hash("Password"))


def populate_with_retries(retries):
    try:
        populate_db()

    except OperationalError:
        if retries > 0:
            sleep(5)
            populate_with_retries(retries-1)
        else:
            raise


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([oppenheimer, blue, lord_of_the_rings, toy, customer])
        db.session.commit()


if __name__ == "__main__":
    populate_db()
